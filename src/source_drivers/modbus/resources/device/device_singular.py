from flask_restful import abort, reqparse
from flask_restful.reqparse import request

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase, modbus_device_marshaller
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes


class ModbusDeviceSingular(ModbusDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        patch_parser.add_argument(attr,
                                  type=modbus_device_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, uuid):
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message='Modbus Device not found')
        return modbus_device_marshaller(device, request.args)

    @classmethod
    def put(cls, uuid):
        data = ModbusDeviceSingular.parser.parse_args()
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device is None:
            return modbus_device_marshaller(cls.add_device(uuid, data), request.args)
        else:
            try:
                device.update(**data)
                return modbus_device_marshaller(ModbusDeviceModel.find_by_uuid(uuid), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def patch(cls, uuid):
        data = ModbusDeviceSingular.patch_parser.parse_args()
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                device.update(**data)
                return modbus_device_marshaller(ModbusDeviceModel.find_by_uuid(uuid), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        device = ModbusDeviceModel.find_by_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204
