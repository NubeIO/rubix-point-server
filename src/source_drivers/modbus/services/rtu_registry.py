import logging

from pymodbus.client.sync import ModbusSerialClient as SerialClient

from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType

logger = logging.getLogger(__name__)


class RtuRegistry:
    _instance = None

    @staticmethod
    def get_instance():
        if not RtuRegistry._instance:
            RtuRegistry()
        return RtuRegistry._instance

    @staticmethod
    def get_rtu_connections():
        return RtuRegistry.get_instance().rtu_connections

    def __init__(self):
        if RtuRegistry._instance:
            raise Exception(" RtuRegistry class is a singleton class!")
        else:
            RtuRegistry._instance = self
            self.rtu_connections = {}

    def register(self):
        logger.info("Called RTU Poll registration")
        network_service = RtuRegistry.get_instance()
        for network in ModbusNetworkModel.query.filter_by(type=ModbusType.RTU):
            network_service.add_network(network)
        logger.info("Finished registration")

    def add_network(self, network) -> SerialClient:
        port = network.rtu_port
        baudrate = network.rtu_speed
        stopbits = network.rtu_stop_bits
        parity = network.rtu_parity.name
        bytesize = network.rtu_byte_size
        timeout = network.timeout

        self.remove_connection_if_exist(port, baudrate, stopbits, parity, bytesize, timeout)
        connection = self.add_connection(port, baudrate, stopbits, parity, bytesize, timeout)
        return connection

    # TODO retries=0, retry_on_empty=False fix these up
    def add_connection(self, port, baudrate, stopbits, parity, bytesize, timeout) -> SerialClient:
        method = 'rtu'
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
        logger.debug(f'Adding rtu_connection {key}')
        self.rtu_connections[key] = SerialClient(method=method, port=port, baudrate=baudrate, stopbits=stopbits,
                                                 parity=parity, bytesize=bytesize, timeout=timeout, retries=0,
                                                 retry_on_empty=False)
        self.rtu_connections[key].connect()
        return self.rtu_connections[key]

    def remove_connection_if_exist(self, port, baudrate, stopbits, parity, bytesize, timeout):
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
        logger.debug(f'Removing rtu_connection {key}')
        rtu_connection = self.rtu_connections.get(key)
        if rtu_connection:
            rtu_connection.close()

    @staticmethod
    def create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout):
        return f'{port}:{baudrate}:{stopbits}:{parity}:{bytesize}:{timeout}'

    @staticmethod
    def create_connection_key_by_network(network):
        port = network.rtu_port
        baudrate = network.rtu_speed
        stopbits = network.rtu_stop_bits
        parity = network.rtu_parity.name
        bytesize = network.rtu_byte_size
        timeout = network.timeout
        return RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
