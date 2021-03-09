import logging
import time
from abc import abstractmethod
from typing import Union, List

from pymodbus.client.sync import BaseModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from sqlalchemy.orm.exc import ObjectDeletedError

from src import db, FlaskThread
from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.services.modbus_registry import ModbusRegistryConnection, ModbusRegistry
from src.drivers.modbus.services.modbus_rtu_registry import ModbusRtuRegistry
from src.drivers.modbus.services.modbus_tcp_registry import ModbusTcpRegistry, ModbusTcpRegistryKey
from src.drivers.modbus.services.polling.poll import poll_point
from src.event_dispatcher import EventDispatcher
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, EventType, HandledByDifferentServiceException, Event

logger = logging.getLogger(__name__)


class ModbusPolling(EventServiceBase):
    __polling_interval: int = 2
    __count: int = 0

    def __init__(self, network_type: ModbusType):
        super().__init__(Drivers.MODBUS.name, True)
        self.__network_type = network_type
        self.supported_events[EventType.INTERNAL_SERVICE_TIMEOUT] = True
        self.supported_events[EventType.CALLABLE] = True
        EventDispatcher().add_driver(self)

    def polling(self):
        self._set_internal_service_timeout(1)
        self.__log_info("Polling started")
        while True:
            event: Event = self._event_queue.get()
            if event.event_type is EventType.INTERNAL_SERVICE_TIMEOUT:
                self.__poll()
                self._set_internal_service_timeout(ModbusPolling.__polling_interval)
            elif event.event_type is EventType.CALLABLE:
                self._handle_internal_callable(event)
            else:
                self._handle_internal_callable(event)

    def __poll(self):
        self.__count += 1
        self.__log_debug(f'Poll loop {self.__count}...')
        networks: List[ModbusNetworkModel] = self.__get_all_networks()
        available_keys: List[str] = []
        for network in networks:
            registry_key = ModbusTcpRegistryKey(network)  # you can use TCP or RTU, choice is yours
            available_keys.append(registry_key.key)
            self.__poll_network(network)

        for key in self.get_registry().get_connections().keys():
            if key not in available_keys:
                self.get_registry().remove_connection_if_exist(key)
        db.session.commit()

    def __poll_network(self, network: ModbusNetworkModel):
        current_connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network)
        if not current_connection.is_running:
            FlaskThread(target=self.__poll_network_thread, daemon=True,
                        kwargs={'network': network}).start()

    def __poll_network_thread(self, network: ModbusNetworkModel):
        """
        Poll connection points on a thread
        """
        self.__log_debug(f'Starting thread for {network}')
        while True:
            current_connection: Union[ModbusRegistryConnection, None] = \
                self.get_registry().get_connection(network)
            if not current_connection:
                self.__log_debug(f'Stopping thread for {network}, no connection')
                break
            network: Union[ModbusNetworkModel, None] = self.__get_network(network.uuid)
            if not network:
                self.__log_debug(f'Stopping thread for {network}, network not found')
                return
            try:
                self.__poll_network_devices(current_connection, network)
            except Exception as e:
                self.__log_error(str(e))
                time.sleep(network.polling_interval_runtime)

    def __poll_network_devices(self, current_connection, network: ModbusNetworkModel):
        current_connection.is_running = True
        devices: List[ModbusDeviceModel] = self.__get_network_devices(network.uuid)
        for device in devices:
            if not self.__ping_point(current_connection, network, device):
                # we suppose that device is offline, so we are not wasting time for looping
                continue
            points: List[ModbusPointModel] = self.__get_all_device_points(device.uuid)
            for point in points:
                try:
                    self.__poll_point(current_connection.client, network, device, point, True)
                except ConnectionException:
                    break
                except ModbusIOException:
                    continue
                time.sleep(float(network.point_interval_ms_between_points) / 1000)
        db.session.commit()
        time.sleep(network.polling_interval_runtime)

    def __ping_point(self, current_connection: ModbusRegistryConnection, network: ModbusNetworkModel,
                     device: ModbusDeviceModel) -> bool:
        """
        Poll connection points
        Checks whether the pinging point is fine or not?
        """
        if device.ping_point:
            try:
                ping_point = ModbusPointModel.create_temporary_from_string(device.ping_point)
                self.__poll_point(current_connection.client, network, device, ping_point, True, False)
            except (ConnectionException, ModbusIOException):
                return False
            except ValueError as e:
                logger.error(f'Modbus device ping_point error: {e}')
                return False
        return True

    def __get_all_networks(self) -> List[ModbusNetworkModel]:
        return ModbusNetworkModel.query.filter_by(type=self.__network_type, enable=True).all()

    @staticmethod
    def __get_network(network_uuid: str) -> Union[ModbusNetworkModel, None]:
        return ModbusNetworkModel.query.filter_by(uuid=network_uuid, enable=True).first()

    @staticmethod
    def __get_network_devices(network_uuid: str) -> List[ModbusDeviceModel]:
        return ModbusDeviceModel.query.filter_by(network_uuid=network_uuid, enable=True).all()

    @staticmethod
    def __get_all_device_points(device_uuid: str) -> List[ModbusPointModel]:
        return ModbusPointModel.query.filter_by(device_uuid=device_uuid, enable=True).all()

    def poll_point_not_existing(self, point: ModbusPointModel, device: ModbusDeviceModel, network: ModbusNetworkModel):
        self.__log_debug(f'Manual poll request Non Existing Point {point}')
        connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network)
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
        connection: ModbusRegistryConnection = self.get_registry().add_edit_and_get_connection(network)
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

    def __log_info(self, message: str):
        logger.info(f'{self.__network_type.name}: {message}')

    def __log_error(self, message: str):
        logger.error(f'{self.__network_type.name}: {message}')

    def __log_debug(self, message: str):
        logger.debug(f'{self.__network_type.name}: {message}')


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
