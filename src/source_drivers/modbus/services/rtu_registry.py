import logging
from typing import Dict

from pymodbus.client.sync import ModbusSerialClient as SerialClient

from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.utils import Singleton

logger = logging.getLogger(__name__)


class RtuRegistry(metaclass=Singleton):

    def __init__(self):
        self.__rtu_connections: Dict[str, SerialClient] = {}

    def get_rtu_connections(self) -> Dict[str, SerialClient]:
        return self.__rtu_connections

    def register(self):
        logger.info("Called RTU Poll registration")
        for network in ModbusNetworkModel.query.filter_by(type=ModbusType.RTU):
            self.add_connection(network)
        logger.info("Finished registration")

    def add_connection(self, network) -> SerialClient:
        port = network.rtu_port
        baudrate = network.rtu_speed
        stopbits = network.rtu_stop_bits
        parity = network.rtu_parity.name
        bytesize = network.rtu_byte_size
        timeout = network.timeout

        self.remove_connection_if_exist(port, baudrate, stopbits, parity, bytesize, timeout)
        connection = self._add_connection(port, baudrate, stopbits, parity, bytesize, timeout)
        return connection

    # TODO retries=0, retry_on_empty=False fix these up
    def _add_connection(self, port, baudrate, stopbits, parity, bytesize, timeout) -> SerialClient:
        method = 'rtu'
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
        logger.debug(f'Adding rtu_connection {key}')
        self.__rtu_connections[key] = SerialClient(method=method, port=port, baudrate=baudrate, stopbits=stopbits,
                                                   parity=parity, bytesize=bytesize, timeout=timeout, retries=0,
                                                   retry_on_empty=False)
        self.__rtu_connections[key].connect()
        return self.__rtu_connections[key]

    def remove_connection_if_exist(self, port, baudrate, stopbits, parity, bytesize, timeout):
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
        logger.debug(f'Removing rtu_connection {key}')
        rtu_connection = self.__rtu_connections.get(key)
        if rtu_connection:
            rtu_connection.close()

    @staticmethod
    def create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout) -> str:
        return f'{port}:{baudrate}:{stopbits}:{parity}:{bytesize}:{timeout}'

    @staticmethod
    def create_connection_key_by_network(network) -> str:
        port = network.rtu_port
        baudrate = network.rtu_speed
        stopbits = network.rtu_stop_bits
        parity = network.rtu_parity.name
        bytesize = network.rtu_byte_size
        timeout = network.timeout
        return RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
