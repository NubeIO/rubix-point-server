import logging
import time
from datetime import datetime
from typing import List, Dict

from pymodbus.exceptions import ConnectionException, ModbusIOException
from sqlalchemy.orm.exc import ObjectDeletedError

from src import db
from src.event_dispatcher import EventDispatcher
from src.handlers.exception import exception_handler
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, EventType, HandledByDifferentServiceException
from src.source_drivers import MODBUS_SERVICE_NAME
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from .modbus_functions.polling.poll import poll_point
from .polling_registry import PoolingRegistry
from .rtu_registry import RtuRegistry
from .tcp_registry import TcpRegistry

logger = logging.getLogger(__name__)


class ModbusPolling(EventServiceBase):
    _polling_period = 2
    _count = 0

    def __init__(self, network_type: ModbusType):
        super().__init__(MODBUS_SERVICE_NAME, True)
        self.__network_type = network_type
        self.supported_events[EventType.INTERNAL_SERVICE_TIMEOUT] = True
        self.supported_events[EventType.CALLABLE] = True
        EventDispatcher().add_source_driver(self)

    def polling(self):
        self._set_internal_service_timeout(1)
        logger.info(f"MODBUS: {self.__network_type.name} Polling started")
        while True:
            event = self._event_queue.get()
            if event.event_type is EventType.INTERNAL_SERVICE_TIMEOUT:
                self.__poll()
                self._set_internal_service_timeout(ModbusPolling._polling_period)
            elif event.event_type is EventType.CALLABLE:
                self._handle_internal_callable(event)
            else:
                self._handle_internal_callable(event)

    @exception_handler
    def __poll(self):
        self._count += 1
        self.__log_debug(f'Poll loop {self._count}...')
        poll_time = time.perf_counter()
        poll_start_time = datetime.now()
        results = self.__get_all_networks_and_devices()
        unavailable_networks = []
        current_network = None
        current_connection = None
        point_stats: List[Dict[str, str]] = []
        for row in results:
            network, device = row
            point_stats: List[Dict[str, str]] = []
            """
            Create and test network connection
            """
            if network.uuid in unavailable_networks:
                continue
            if current_network != network:
                current_connection = self._get_connection(network, device)
                current_network = network
            if device.ping_point:
                try:
                    ping_point = ModbusPointModel.create_temporary_from_string(device.ping_point)
                    self.__poll_point(current_connection, ping_point, device, network, True, False)
                except ConnectionException:
                    unavailable_networks.append(network.uuid)
                    continue
                except ModbusIOException:
                    continue
                except ValueError as e:
                    logger.error(f'Modbus device ping_point error: {e}')
            """
            Poll device points if connection successful
            """
            points = self.__get_all_device_points(device.uuid)
            for point in points:
                if self.event_count() > 0:
                    self.__log_debug('Breaking poll loop due to queued event')
                    return
                try:
                    self.__poll_point(current_connection, point, device, network, True)
                except ConnectionException:
                    unavailable_networks.append(network.uuid)
                    point_stats.append({'uuid': point.uuid, "status": 'Fail'})
                    break
                except ModbusIOException:
                    point_stats.append({'uuid': point.uuid, "status": 'Fail'})
                    continue
            db.session.commit()
        poll_time = time.perf_counter() - poll_time
        poll_end_time = datetime.now()
        if self._count == 1:
            PoolingRegistry().update({'start_time': f'{poll_start_time}'})

        PoolingRegistry().update({
            'poll_start_time': str(poll_start_time),
            'poll_end_time': str(poll_end_time),
            'poll_complete_time': f'{round(poll_time, 3)} secs',
            'loop_count': self._count,
            'point_stats': point_stats
        })

        self.__log_debug(f'Poll loop {self._count} time: {round(poll_time, 3)} secs')

    def __get_all_networks_and_devices(self):
        results = db.session.query(ModbusNetworkModel, ModbusDeviceModel). \
            select_from(ModbusNetworkModel).filter_by(type=self.__network_type, enable=True) \
            .join(ModbusDeviceModel).filter_by(type=self.__network_type, enable=True) \
            .all()
        return results

    def __get_all_device_points(self, device_uuid: str):
        results = db.session.query(ModbusPointModel).filter_by(device_uuid=device_uuid, enable=True) \
            .all()
        return results

    def poll_point_not_existing(self, point: ModbusPointModel, device: ModbusDeviceModel, network: ModbusNetworkModel):
        self.__log_debug(f'Manual poll request Non Existing Point {point}')
        connection = self._get_connection(network, device)
        if network.type is not self.__network_type:
            raise HandledByDifferentServiceException
        point_store = self.__poll_point(connection, point, device, network, False, False)
        return point_store

    def poll_point(self, point: ModbusPointModel) -> ModbusPointModel:
        self.__log_debug(f'Manual poll request {point}')
        device = ModbusDeviceModel.find_by_uuid(point.device_uuid)
        if device.type is not self.__network_type:
            raise HandledByDifferentServiceException
        network = ModbusNetworkModel.find_by_uuid(device.network_uuid)
        self.__log_debug(f'Manual poll request: network: {network.uuid}, device: {device.uuid}, point: {point.uuid}')
        connection = self._get_connection(network, device)
        self.__poll_point(connection, point, device, network)
        return point

    def __poll_point(self, connection, point: ModbusPointModel, device: ModbusDeviceModel, network: ModbusNetworkModel,
                     update_all: bool = True, update_point_store: bool = True) -> PointStoreModel:
        point_store = None
        if update_all:
            try:
                error = None
                try:
                    point_store = poll_point(self, connection, network, device, point, update_point_store)
                except ConnectionException as e:
                    if not network.fault:
                        network.set_fault(True)
                    error = e
                except ModbusIOException as e:
                    if not device.fault:
                        device.set_fault(True)
                    error = e

                if network.fault and not isinstance(error, ConnectionException):
                    network.set_fault(False)
                elif device.fault and not isinstance(error, ModbusIOException) and \
                    not isinstance(error, ConnectionException):
                    device.set_fault(False)

                if error is not None:
                    raise error
            except ObjectDeletedError:
                return None
        else:
            point_store = poll_point(self, connection, network, device, point, update_point_store)
        return point_store

    def _get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        raise NotImplementedError

    def __log_debug(self, message: str):
        logger.debug(f'MODBUS: {self.__network_type.name} {message}')


class RtuPolling(ModbusPolling):

    def __init__(self):
        super().__init__(ModbusType.RTU)

    def _get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        registry = RtuRegistry()
        connection = registry.get_rtu_connections().get(RtuRegistry.create_connection_key_by_network(network))
        if not connection:
            connection = registry.add_network(network)
        return connection


class TcpPolling(ModbusPolling):

    def __init__(self):
        super().__init__(ModbusType.TCP)

    def _get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        host = device.tcp_ip
        port = device.tcp_port
        registry = TcpRegistry()
        connection = registry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            connection = registry.add_device(device)
        return connection
