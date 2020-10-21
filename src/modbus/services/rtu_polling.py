import time
from src.modbus.interfaces.point.points import ModbusPointType
from src import db
from src.modbus.models.mod_device import ModbusDeviceModel
from src.modbus.models.mod_network import ModbusNetworkModel, ModbusType
from src.modbus.models.mod_point import ModbusPointModel
from src.modbus.models.mod_point_store import ModbusPointStoreModel
from src.modbus.services.rtu_registry import RtuRegistry
from src.utils.data_funcs import DataHelpers
from src.modbus.services.modbus_functions.modbus_functions import read_holding


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
                self.poll_point(network, device, point)

    def poll_point(self, network, device, point):
        rtu_connection = RtuRegistry.get_rtu_connections().get(RtuRegistry.create_connection_key_by_network(network))
        if not rtu_connection:
            RtuRegistry.get_instance().add_network(network)

        # TODO: whether it's functional or not, don't know how data we read
        reg = point.mod_point_reg
        mod_device_addr = device.mod_device_addr
        mod_point_reg_length = point.mod_point_reg_length
        mod_point_type = point.mod_point_type.name
        mod_point_data_type = point.mod_point_data_type.name
        mod_point_data_endian = point.mod_point_data_endian.name

        try:
            val = None
            print({'mod_device_addr':mod_device_addr, 'reg': reg, 'mod_point_reg_length': mod_point_reg_length, 'mod_point_type': mod_point_type})
            if mod_point_type == ModbusPointType.readCoils:
                val = rtu_connection.read_coils(reg, mod_point_reg_length, unit=mod_device_addr)
                val = val.bits[0]
                # array = val.bits
                val = DataHelpers.bool_to_int(val)
                print("read_coils", val)
            if mod_point_type == ModbusPointType.readHoldingRegisters.name:
                print(11111)

                # def read_holding(client, reg_start, reg_length, _unit, data_type, endian):
                print(3333)
                print(rtu_connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type, mod_point_data_endian)
                val = read_holding(rtu_connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type, mod_point_data_endian)
                # first = val.registers[0]
                # array = val.registers[0:]
                # print("first", first, 'array', array)
                print('val 1111111')
                print(val)

            if val:
                print('done')
                # print("read_holding", val, 'array')
                # print("mod_point_type", mod_point_type, 'reg', reg, 'val', val,'array', array)
                # ModbusPointStoreModel(mod_point_value=val, mod_point_uuid=point.mod_point_uuid).save_to_db()
        except Exception as e:
            print(f'Error: {str(e)}')
