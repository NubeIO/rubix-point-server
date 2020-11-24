from flask_restful import abort, marshal_with, reqparse

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_fields, \
    modbus_device_all_attributes


class ModbusDeviceSingular(ModbusDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        patch_parser.add_argument(attr, type=modbus_device_all_attributes[attr]['type'], required=False)

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
    @marshal_with(modbus_device_all_fields)
    def patch(cls, uuid):
        data = ModbusDeviceSingular.patch_parser.parse_args()
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            network_uuid = data.network_uuid if data.network_uuid else device.network_uuid
            type_ = data.type if data.type else device.type
            cls.abort_if_network_does_not_exist_and_type_mismatch(network_uuid, type_)
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
