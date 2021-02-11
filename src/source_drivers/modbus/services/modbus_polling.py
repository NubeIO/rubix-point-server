import logging
from typing import Union, List, Tuple

from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient, BaseModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from sqlalchemy.orm.exc import ObjectDeletedError

from src import db
from src.event_dispatcher import EventDispatcher
from src.handlers.exception import exception_handler
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, EventType, HandledByDifferentServiceException, Event
from src.source_drivers import MODBUS_SERVICE_NAME
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from .modbus_functions.polling.poll import poll_point
from .rtu_registry import RtuRegistry
from .tcp_registry import TcpRegistry

logger = logging.getLogger(__name__)


class ModbusPolling(EventServiceBase):
    _polling_period: int = 2
    _count: int = 0

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
            event: Event = self._event_queue.get()
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
        results: List[Tuple[ModbusNetworkModel, ModbusDeviceModel]] = self.__get_all_networks_and_devices()
        for row in results:
            network, device = row
            self.__poll_network_device(network, device)

    def __poll_network_device(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        """
        Poll network > device points
        """
        current_connection: BaseModbusClient = self.get_connection(network, device)
        if device.ping_point:
            try:
                ping_point = ModbusPointModel.create_temporary_from_string(device.ping_point)
                self.__poll_point(current_connection, network, device, ping_point, True, False)
            except (ConnectionException, ModbusIOException):
                return
            except ValueError as e:
                logger.error(f'Modbus device ping_point error: {e}')
        """
        Poll network > device points if connection successful when we have device.ping_point
        """
        points: List[ModbusPointModel] = self.__get_all_device_points(device.uuid)
        for point in points:
            if self.event_count() > 0:
                self.__log_debug('Breaking poll loop due to queued event')
                return
            try:
                self.__poll_point(current_connection, network, device, point, True)
            except ConnectionException:
                break
            except ModbusIOException:
                continue
        db.session.commit()

    def __get_all_networks_and_devices(self) -> List[Tuple[ModbusNetworkModel, ModbusDeviceModel]]:
        results = db.session.query(ModbusNetworkModel, ModbusDeviceModel) \
            .select_from(ModbusNetworkModel).filter_by(type=self.__network_type, enable=True) \
            .join(ModbusDeviceModel).filter_by(type=self.__network_type, enable=True) \
            .all()
        return results

    def __get_all_device_points(self, device_uuid: str) -> List[ModbusPointModel]:
        results: List[ModbusPointModel] = db.session.query(ModbusPointModel) \
            .filter_by(device_uuid=device_uuid, enable=True) \
            .all()
        return results

    def poll_point_not_existing(self, point: ModbusPointModel, device: ModbusDeviceModel, network: ModbusNetworkModel):
        self.__log_debug(f'Manual poll request Non Existing Point {point}')
        connection: BaseModbusClient = self.get_connection(network, device)
        if network.type is not self.__network_type:
            raise HandledByDifferentServiceException
        point_store = self.__poll_point(connection, network, device, point, False, False)
        return point_store

    def poll_point(self, point: ModbusPointModel) -> ModbusPointModel:
        self.__log_debug(f'Manual poll request {point}')
        device: ModbusDeviceModel = ModbusDeviceModel.find_by_uuid(point.device_uuid)
        if device.type is not self.__network_type:
            raise HandledByDifferentServiceException
        network: ModbusNetworkModel = ModbusNetworkModel.find_by_uuid(device.network_uuid)
        self.__log_debug(f'Manual poll request: network: {network.uuid}, device: {device.uuid}, point: {point.uuid}')
        connection: BaseModbusClient = self.get_connection(network, device)
        self.__poll_point(connection, network, device, point)
        return point

    def __poll_point(self, connection: BaseModbusClient, network: ModbusNetworkModel, device: ModbusDeviceModel,
                     point: ModbusPointModel, update_all: bool = True,
                     update_point_store: bool = True) -> Union[PointStoreModel, None]:
        point_store: Union[PointStoreModel, None] = None
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

    def get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> BaseModbusClient:
        """
        It returns the connection from the registry, if doesn't exist it will create connection and returns
        """
        raise NotImplementedError

    def __log_debug(self, message: str):
        logger.debug(f'MODBUS: {self.__network_type.name} {message}')


class RtuPolling(ModbusPolling):

    def __init__(self):
        super().__init__(ModbusType.RTU)

    def get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusSerialClient:
        registry = RtuRegistry()
        connection: ModbusSerialClient = registry.get_rtu_connections().get(
            RtuRegistry.create_connection_key_by_network(network))
        if not connection:
            connection = registry.add_connection(network)
        return connection


class TcpPolling(ModbusPolling):

    def __init__(self):
        super().__init__(ModbusType.TCP)

    def get_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusTcpClient:
        host: str = device.tcp_ip
        port: int = device.tcp_port
        registry: TcpRegistry = TcpRegistry()
        connection: ModbusTcpClient = registry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            connection = registry.add_connection(device)
        return connection
