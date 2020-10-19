import time

from src.modbus.models.mod_network import ModbusType, ModbusNetworkModel
from src.modbus.services.tcp_registry import TcpRegistry


class TcpPolling:
    _instance = None
    _polling_period = 2

    @staticmethod
    def get_instance():
        if not TcpPolling._instance:
            TcpPolling()
        return TcpPolling._instance

    def __init__(self):
        if TcpPolling._instance:
            raise Exception("TcpPolling class is a singleton class!")
        else:
            TcpPolling._instance = self

    def polling(self):
        print("TCP Polling started")
        while True:
            time.sleep(2)
            print('looping...')
            for network in ModbusNetworkModel.query.filter_by(mod_network_type=ModbusType.TCP):
                for device in network.mod_devices:
                    if device.mod_device_type is ModbusType.TCP:
                        for point in device.mod_points:
                            self.poll_point(device, point)

    def poll_point(self, device, point):
        host = device.mod_tcp_device_ip
        port = device.mod_tcp_device_port
        tcp_connection = TcpRegistry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not tcp_connection:
            TcpRegistry.get_instance().add_device(device)
        # TODO: confirm whether this column is correct or not
        reg = point.mod_point_reg
        # TODO: Manually put 1 for now
        unit = 1
        try:
            val = tcp_connection.read_holding_registers(reg, 1, unit=unit)
            print('val:', val.registers[0:], 'reg:', reg)
        except Exception as e:
            print(str(e))
