import logging
from abc import abstractmethod
from typing import Dict

from pymodbus.client.sync import BaseModbusClient

from src.source_drivers.modbus.interfaces.network.network import ModbusType
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.utils import Singleton

logger = logging.getLogger(__name__)


class ModbusRegistryKey:
    def __init__(self, network: ModbusNetworkModel, device: ModbusDeviceModel):
        self.network: ModbusNetworkModel = network
        self.device: ModbusDeviceModel = device

        self.key: str = self.create_key()
        self.connection_key: str = self.create_connection_key()

    def create_key(self):
        return f'{self.network.uuid}:{self.device.uuid}'

    @abstractmethod
    def create_connection_key(self) -> str:
        raise NotImplementedError


class ModbusRegistryConnection:
    def __init__(self, connection_key: str, client: BaseModbusClient):
        self.connection_key: str = connection_key
        self.client: BaseModbusClient = client
        self.is_running: bool = False
        self.is_deleted: bool = False


class ModbusRegistry(metaclass=Singleton):
    """
    Connection format
    {
      "<key1>": "<RtuConnection1>",
      "<key2>": "<RtuConnection2>"
    }
    """

    def __init__(self):
        self.connections: Dict[str, ModbusRegistryConnection] = {}

    def get_connections(self) -> Dict[str, ModbusRegistryConnection]:
        return self.connections

    def get_connection(self, network, device) -> ModbusRegistryConnection:
        registry_key: ModbusRegistryKey = self.get_registry_key(network, device)
        return self.connections.get(registry_key.key)

    def add_edit_and_get_connection(self, network: ModbusNetworkModel,
                                    device: ModbusDeviceModel) -> ModbusRegistryConnection:
        registry_key: ModbusRegistryKey = self.get_registry_key(network, device)
        connection: ModbusRegistryConnection = self.connections.get(registry_key.key)
        if connection and connection.connection_key != registry_key.connection_key:
            connection = self.__class__().add_connection(network, device)
        if not connection:
            connection = self.__class__().add_connection(network, device)
        return connection

    def register(self):
        logger.info(f"Called {self.get_type().name} poll registration")
        for network in ModbusNetworkModel.query.filter_by(type=self.get_type()):
            self.initialize_network_connections(network)
        logger.info(f"Finished {self.get_type().name} poll registration")

    def initialize_network_connections(self, network: ModbusNetworkModel):
        for device in network.devices:
            if device.type is ModbusType.TCP:
                self.add_connection(network, device)

    @abstractmethod
    def add_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusRegistryConnection:
        raise NotImplementedError

    def remove_connection_if_exist(self, key):
        logger.debug(f'Removing rtu_connection {key}')
        connection = self.connections.get(key)
        if connection:
            connection.client.close()
            del self.connections[key]

    @abstractmethod
    def get_registry_key(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusRegistryKey:
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> ModbusType:
        raise NotImplementedError
