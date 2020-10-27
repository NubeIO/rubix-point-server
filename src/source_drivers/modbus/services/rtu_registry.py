import logging

from pymodbus.client.sync import ModbusSerialClient as SerialClient

from src.source_drivers.modbus.services.modbus_functions.debug import modbus_pymodbus_logs, modbus_start_up

if modbus_pymodbus_logs:
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType


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
            raise Exception(" MODBUS: RtuRegistry class is a singleton class!")
        else:
            RtuRegistry._instance = self
            self.rtu_connections = {}

    def register(self):
        if modbus_start_up:
            print("MODBUS: Called RTU Poll registration")
        network_service = RtuRegistry.get_instance()
        for network in ModbusNetworkModel.query.filter_by(type=ModbusType.RTU):
            network_service.add_network(network)
        if modbus_start_up:
            print("MODBUS: Finished registration")

    def add_network(self, network):
        port = network.rtu_port
        baudrate = network.rtu_speed
        stopbits = network.rtu_stopbits
        parity = network.rtu_parity.name
        bytesize = network.rtu_bytesize
        timeout = network.timeout

        self.remove_connection_if_exist(port, baudrate, stopbits, parity, bytesize, timeout)
        self.add_connection(port, baudrate, stopbits, parity, bytesize, timeout)

    # TODO retries=0, retry_on_empty=False fix these up
    def add_connection(self, port, baudrate, stopbits, parity, bytesize, timeout):
        method = 'rtu'
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
        self.rtu_connections[key] = SerialClient(method=method, port=port, baudrate=baudrate, stopbits=stopbits,
                                                 parity=parity, bytesize=bytesize, timeout=timeout, retries=0,
                                                 retry_on_empty=False)
        self.rtu_connections[key].connect()

    def remove_connection_if_exist(self, port, baudrate, stopbits, parity, bytesize, timeout):
        key = RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
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
        stopbits = network.rtu_stopbits
        parity = network.rtu_parity.name
        bytesize = network.rtu_bytesize
        timeout = network.timeout
        return RtuRegistry.create_connection_key(port, baudrate, stopbits, parity, bytesize, timeout)
