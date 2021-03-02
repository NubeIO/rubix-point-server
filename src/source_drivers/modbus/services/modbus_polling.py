import logging
import time
from abc import abstractmethod
from typing import Union, List, Tuple

from pymodbus.client.sync import BaseModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from sqlalchemy.orm.exc import ObjectDeletedError

from src import db, FlaskThread
from src.event_dispatcher import EventDispatcher
from src.handlers.exception import exception_handler
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, EventType, HandledByDifferentServiceException, Event
from src.source_drivers import MODBUS_SERVICE_NAME
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from .modbus_functions.polling.poll import poll_point
from .modbus_registry import ModbusRegistryConnection, ModbusRegistry
from .modbus_rtu_registry import ModbusRtuRegistry
from .modbus_tcp_registry import ModbusTcpRegistry, ModbusTcpRegistryKey

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
        available_keys: List[str] = []
        for row in results:
            network, device = row
            registry_key = ModbusTcpRegistryKey(network, device)  # you can use TCP or RTU, choice is yours
            available_keys.append(registry_key.key)
            self.__poll_network_device(network, device)

        for key in self.get_registry().get_connections().keys():
            if key not in available_keys:
                self.get_registry().remove_connection_if_exist(key)

    def __poll_network_device(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        """
        Poll network > device points
        """
        current_connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network, device)
        if device.ping_point:
            try:
                ping_point = ModbusPointModel.create_temporary_from_string(device.ping_point)
                self.__poll_point(current_connection.client, network, device, ping_point, True, False)
            except (ConnectionException, ModbusIOException):
                return
            except ValueError as e:
                logger.error(f'Modbus device ping_point error: {e}')
        if not current_connection.is_running:
            FlaskThread(target=self.__poll_network_device_thread, daemon=True,
                        kwargs={'network': network,
                                'device': device
                                }).start()

    def __poll_network_device_thread(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        """
        Poll network > device points if connection successful when we have device.ping_point
        """
        while True:
            current_connection: Union[ModbusRegistryConnection, None] = \
                self.get_registry().get_connection(network, device)
            if not current_connection:
                self.__log_debug(f'Stopping thread for {network} {device}')
                break
            current_connection.is_running = True
            points: List[ModbusPointModel] = self.__get_all_device_points(device.uuid)
            for point in points:
                try:
                    self.__poll_point(current_connection.client, network, device, point, True)
                except ConnectionException:
                    break
                except ModbusIOException:
                    continue
                time.sleep(float(device.point_interval_ms_between_points) / 1000)
            db.session.commit()
            time.sleep(device.polling_interval_runtime)

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
        connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network, device)
        if network.type is not self.__network_type:
            raise HandledByDifferentServiceException
        point_store = self.__poll_point(connection.client, network, device, point, False, False)
        return point_store

    def poll_point(self, point: ModbusPointModel) -> ModbusPointModel:
        self.__log_debug(f'Manual poll request {point}')
        device: ModbusDeviceModel = ModbusDeviceModel.find_by_uuid(point.device_uuid)
        if device.type is not self.__network_type:
            raise HandledByDifferentServiceException
        network: ModbusNetworkModel = ModbusNetworkModel.find_by_uuid(device.network_uuid)
        self.__log_debug(f'Manual poll request: network: {network.uuid}, device: {device.uuid}, point: {point.uuid}')
        connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network, device)
        self.__poll_point(connection.client, network, device, point)
        return point

    def __poll_point(self, client: BaseModbusClient, network: ModbusNetworkModel, device: ModbusDeviceModel,
                     point: ModbusPointModel, update_all: bool = True,
                     update_point_store: bool = True) -> Union[PointStoreModel, None]:
        point_store: Union[PointStoreModel, None] = None
        if update_all:
            try:
                error = None
                try:
                    point_store = poll_point(self, client, network, device, point, update_point_store)
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
            point_store = poll_point(self, client, network, device, point, update_point_store)
        return point_store

    @abstractmethod
    def get_registry(self) -> ModbusRegistry:
        raise NotImplementedError

    def __log_debug(self, message: str):
        logger.debug(f'MODBUS: {self.__network_type.name} {message}')


class RtuPolling(ModbusPolling, ):

    def __init__(self):
        super().__init__(ModbusType.RTU)

    @abstractmethod
    def get_registry(self) -> ModbusRegistry:
        return ModbusRtuRegistry()


class TcpPolling(ModbusPolling):

    def __init__(self):
        super().__init__(ModbusType.TCP)

    @abstractmethod
    def get_registry(self) -> ModbusRegistry:
        return ModbusTcpRegistry()
