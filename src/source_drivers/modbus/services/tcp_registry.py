import logging

from pymodbus.client.sync import ModbusTcpClient

from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType

logger = logging.getLogger(__name__)


class TcpRegistry:
    _instance = None

    @staticmethod
    def get_instance():
        if not TcpRegistry._instance:
            TcpRegistry()
        return TcpRegistry._instance

    @staticmethod
    def get_tcp_connections():
        return TcpRegistry.get_instance().tcp_connections

    def __init__(self):
        if TcpRegistry._instance:
            raise Exception("TcpRegistry class is a singleton class!")
        else:
            TcpRegistry._instance = self
            self.tcp_connections = {}

    def register(self):
        logger.info("Called TCP Poll registration")
        network_service = TcpRegistry.get_instance()
        for network in ModbusNetworkModel.query.filter_by(type=ModbusType.TCP):
            network_service.initialize_network_connections(network)
        logger.info("Finished registration")

    def initialize_network_connections(self, network):
        for device in network.devices:
            if device.type is ModbusType.TCP:
                self.add_device(device)

    def add_device(self, device):
        host = device.tcp_ip
        port = device.tcp_port
        self.remove_connection_if_exist(host, port)
        self.add_connection(host, port)

    def add_connection(self, host, port):
        key = TcpRegistry.create_connection_key(host, port)
        logger.debug(f'Adding tcp_connection {key}')
        self.tcp_connections[key] = ModbusTcpClient(host, port)

    def remove_connection_if_exist(self, host, port):
        key = TcpRegistry.create_connection_key(host, port)
        logger.debug(f'Removing tcp_connection {key}')
        tcp_connection = self.tcp_connections.get(key)
        if tcp_connection:
            tcp_connection.close()

    @staticmethod
    def create_connection_key(host, port):
        return f'{host}:{port}'
