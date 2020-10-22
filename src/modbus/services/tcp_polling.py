import time
from src import db
from src.modbus.models.device import ModbusDeviceModel
from src.modbus.models.network import ModbusNetworkModel, ModbusType
from src.modbus.models.point import ModbusPointModel
from src.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.modbus.services.modbus_functions.poll import poll_point


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
        if modbus_debug_poll:
            print("MODBUS TCP Polling started")
        count = 0
        while True:
            time.sleep(TcpPolling._polling_period)
            count += 1
            print(f'Looping TCP {count}...')
            # TODO: Implement caching
            results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                select_from(ModbusNetworkModel).filter_by(type=ModbusType.TCP) \
                .join(ModbusDeviceModel).filter_by(type=ModbusType.TCP) \
                .join(ModbusPointModel).all()
            db.session.close()
            for network, device, point in results:
                poll_point(network, device, point, 'tcp')
