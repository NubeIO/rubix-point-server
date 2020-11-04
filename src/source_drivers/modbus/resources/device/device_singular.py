from flask_restful import abort, marshal_with

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_fields


class ModbusDeviceSingular(ModbusDeviceBase):
    @classmethod
    @marshal_with(modbus_device_all_fields)
    def get(cls, uuid):
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message='Modbus Device not found')
        return device

    @classmethod
    @marshal_with(modbus_device_all_fields)
    def put(cls, uuid):
        data = ModbusDeviceSingular.parser.parse_args()
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device is None:
            return cls.add_device(uuid, data)
        else:
            cls.abort_if_network_does_not_exist_and_type_mismatch(data.network_uuid, data.type)
            try:
                device.update(**data)
                return ModbusDeviceModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204
