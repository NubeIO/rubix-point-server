import time

from src import db
from src.modbus.models.mod_device import ModbusDeviceModel
from src.modbus.models.mod_network import ModbusNetworkModel
from src.modbus.models.mod_point import ModbusPointModel
from src.modbus.models.mod_point_store import ModbusPointStoreModel
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
        count = 0
        while True:
            time.sleep(2)
            count += 1
            print(f'Looping {count}...')
            results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                select_from(ModbusNetworkModel).join(ModbusDeviceModel).join(ModbusPointModel).all()
            for network, device, point in results:
                self.poll_point(device, point)

            # for network in ModbusNetworkModel.query.filter_by(mod_network_type=ModbusType.TCP):
            #     print("network", network)
            #     for device in network.mod_devices:
            #         print("device", device)
            #         if device.mod_device_type is ModbusType.TCP:
            #             for point in device.mod_points:
            #                 self.poll_point(device, point)

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
            val = val.registers[0]
            print('val:', val, 'reg:', reg)
            ModbusPointStoreModel(mod_point_value=val, mod_point_uuid=point.mod_point_uuid).save_to_db()
        except Exception as e:
            print(str(e))
