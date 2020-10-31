import uuid
from flask_restful import marshal_with

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_fields


class ModbusDevicePlural(ModbusDeviceBase):
    @classmethod
    @marshal_with(modbus_device_all_fields, envelope="devices")
    def get(cls):
        return ModbusDeviceModel.query.all()

    @classmethod
    @marshal_with(modbus_device_all_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = ModbusDevicePlural.parser.parse_args()
        return cls.add_device(_uuid, data)
