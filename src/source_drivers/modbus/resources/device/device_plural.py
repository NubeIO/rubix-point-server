from flask_restful.reqparse import request

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase, modbus_device_marshaller


class ModbusDevicePlural(ModbusDeviceBase):
    @classmethod
    def get(cls):
        return modbus_device_marshaller(ModbusDeviceModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = ModbusDevicePlural.parser.parse_args()
        return modbus_device_marshaller(cls.add_device(data), request.args)
