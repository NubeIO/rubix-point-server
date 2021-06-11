import logging
from abc import abstractmethod
from typing import Dict

import shortuuid
from pymodbus.client.sync import BaseModbusClient

from src.drivers.modbus.enums.network.network import ModbusType
from src.drivers.modbus.models.network import ModbusNetworkModel
from src.utils import Singleton

logger = logging.getLogger(__name__)


class ModbusRegistryKey:
    def __init__(self, network: ModbusNetworkModel):
        self.network: ModbusNetworkModel = network

        self.key: str = self.create_key()
        self.connection_key: str = self.create_connection_key()

    def create_key(self):
        return self.network.uuid or shortuuid.uuid()  # there will be no uuid on poll_point

    @abstractmethod
    def create_connection_key(self) -> str:
        raise NotImplementedError


class ModbusRegistryConnection:
    def __init__(self, connection_key: str, client: BaseModbusClient):
        self.connection_key: str = connection_key
        self.client: BaseModbusClient = client
        self.is_running: bool = False


class ModbusRegistry(metaclass=Singleton):
    """
    Connection format
    {
      "<key1>": "<ModbusRegistryConnection1>",
      "<key2>": "<ModbusRegistryConnection2>"
    }
    """

    def __init__(self):
        self.connections: Dict[str, ModbusRegistryConnection] = {}

    def get_connections(self) -> Dict[str, ModbusRegistryConnection]:
        return self.connections

    def get_connection(self, network) -> ModbusRegistryConnection:
        registry_key: ModbusRegistryKey = self.get_registry_key(network)
        return self.connections.get(registry_key.key)

    def add_edit_and_get_connection(self, network: ModbusNetworkModel) -> ModbusRegistryConnection:
        registry_key: ModbusRegistryKey = self.get_registry_key(network)
        connection: ModbusRegistryConnection = self.connections.get(registry_key.key)
        if connection and connection.connection_key != registry_key.connection_key:
            # connection has some changes
            connection = self.__class__().add_connection(network)
        if not connection:
            # creating connection for the first time
            connection = self.__class__().add_connection(network)
        return connection

    def register(self):
        logger.info(f"Called {self.get_type().name} poll registration")
        for network in ModbusNetworkModel.query.filter_by(type=self.get_type()):
            self.initialize_network_connections(network)
        logger.info(f"Finished {self.get_type().name} poll registration")

    def initialize_network_connections(self, network: ModbusNetworkModel):
        for device in network.devices:
            if device.type is ModbusType.TCP:
                self.add_connection(network)

    @abstractmethod
    def add_connection(self, network: ModbusNetworkModel) -> ModbusRegistryConnection:
        raise NotImplementedError

    def remove_connection_if_exist(self, key):
        logger.debug(f'Removing rtu_connection {key}')
        connection: ModbusRegistryConnection = self.connections.get(key)
        if connection:
            connection.client.close()
            del self.connections[key]

    @abstractmethod
    def get_registry_key(self, network: ModbusNetworkModel) -> ModbusRegistryKey:
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> ModbusType:
        raise NotImplementedError
