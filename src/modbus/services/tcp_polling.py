import time
from src.modbus.interfaces.point.points import ModbusPointType
from src import db
from src.modbus.models.mod_device import ModbusDeviceModel
from src.modbus.models.mod_network import ModbusNetworkModel, ModbusType
from src.modbus.models.mod_point import ModbusPointModel
from src.modbus.models.mod_point_store import ModbusPointStoreModel
from src.modbus.services.modbus_functions.poll import poll_point
from src.modbus.services.tcp_registry import TcpRegistry
from src.utils.data_funcs import DataHelpers


class TcpPolling:
    _instance = None
    _polling_period = 5

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
            time.sleep(TcpPolling._polling_period)
            count += 1
            print(f'Looping TCP {count}...')
            # TODO: Implement caching
            results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                select_from(ModbusNetworkModel).filter_by(mod_network_type=ModbusType.TCP).join(
                ModbusDeviceModel).filter_by(mod_device_type=ModbusType.TCP).join(
                ModbusPointModel).all()
            for network, device, point in results:
                poll_point(network, device, point, 'tcp')
