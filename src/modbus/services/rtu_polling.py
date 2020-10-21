import time
from src import db
from src.modbus.models.mod_device import ModbusDeviceModel
from src.modbus.models.mod_network import ModbusNetworkModel, ModbusType
from src.modbus.models.mod_point import ModbusPointModel
from src.modbus.services.modbus_functions.poll import poll_point


class RtuPolling:
    _instance = None
    _polling_period = 5

    @staticmethod
    def get_instance():
        if not RtuPolling._instance:
            RtuPolling()
        return RtuPolling._instance

    def __init__(self):
        if RtuPolling._instance:
            raise Exception("RtuPolling class is a singleton class!")
        else:
            RtuPolling._instance = self

    def polling(self):
        print("RTU Polling started")
        count = 0
        while True:
            time.sleep(RtuPolling._polling_period)
            count += 1
            print(f'Looping RTU {count}...')
            # TODO: Implement caching
            results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                select_from(ModbusNetworkModel).filter_by(mod_network_type=ModbusType.RTU).join(
                ModbusDeviceModel).filter_by(mod_device_type=ModbusType.RTU).join(
                ModbusPointModel).all()
            for network, device, point in results:
                poll_point(network, device, point, 'rtu')
