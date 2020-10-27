from src import db
from src.sourceDrivers.modbus.models.device import ModbusDeviceModel
from src.sourceDrivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.sourceDrivers.modbus.models.point import ModbusPointModel
from src.sourceDrivers.modbus.services.modbus_functions.debug import modbus_polling_count
from src.sourceDrivers.modbus.services.modbus_functions.polling.poll import poll_point
import time


class RtuPolling:
    _instance = None
    _polling_period = 0.2

    @staticmethod
    def get_instance():
        if not RtuPolling._instance:
            RtuPolling()
        return RtuPolling._instance

    def __init__(self):
        if RtuPolling._instance:
            raise Exception("MODBUS: RtuPolling class is a singleton class!")
        else:
            RtuPolling._instance = self

    def polling(self):
        if modbus_polling_count:
            print("RTU Polling started")
        count = 0
        while True:
            time.sleep(RtuPolling._polling_period)
            count += 1
            if modbus_polling_count:
                print(f'MODBUS: Looping RTU {count}...')

            # TODO: Implement caching
            results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                select_from(ModbusNetworkModel).filter_by(type=ModbusType.RTU) \
                .join(ModbusDeviceModel).filter_by(type=ModbusType.RTU) \
                .join(ModbusPointModel).all()

            for network, device, point in results:
                poll_point(network, device, point, ModbusType.RTU)
            db.session.commit()
