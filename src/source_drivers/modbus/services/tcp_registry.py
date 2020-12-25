import logging

from pymodbus.client.sync import ModbusTcpClient

from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.utils import Singleton

logger = logging.getLogger(__name__)


class TcpRegistry(metaclass=Singleton):

    def __init__(self):
        self.__tcp_connections = {}

    def get_tcp_connections(self):
        return self.__tcp_connections

    def register(self):
        logger.info("Called TCP Poll registration")
        for network in ModbusNetworkModel.query.filter_by(type=ModbusType.TCP):
            self.initialize_network_connections(network)
        logger.info("Finished registration")

    def initialize_network_connections(self, network):
        for device in network.devices:
            if device.type is ModbusType.TCP:
                self.add_device(device)

    def add_device(self, device) -> ModbusTcpClient:
        host = device.tcp_ip
        port = device.tcp_port
        self.remove_connection_if_exist(host, port)
        connection = self.add_connection(host, port)
        return connection

    def add_connection(self, host, port) -> ModbusTcpClient:
        key = TcpRegistry.create_connection_key(host, port)
        logger.debug(f'Adding tcp_connection {key}')
        self.__tcp_connections[key] = ModbusTcpClient(host, port)
        return self.__tcp_connections[key]

    def remove_connection_if_exist(self, host, port):
        key = TcpRegistry.create_connection_key(host, port)
        logger.debug(f'Removing tcp_connection {key}')
        tcp_connection = self.__tcp_connections.get(key)
        if tcp_connection:
            tcp_connection.close()

    @staticmethod
    def create_connection_key(host, port):
        return f'{host}:{port}'
