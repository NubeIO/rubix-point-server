from flask_restful import abort, reqparse
from flask_restful.reqparse import request

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_base import ModbusDeviceBase, modbus_device_marshaller
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes


class ModbusDeviceSingularBase(ModbusDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        patch_parser.add_argument(attr,
                                  type=modbus_device_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if not device:
            abort(404, message='Modbus Device not found')
        return modbus_device_marshaller(device, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if device is None:
            return modbus_device_marshaller(cls.add_device(data), request.args)
        else:
            try:
                device.update(**data)
                return modbus_device_marshaller(cls.get_device(**kwargs), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if device is None:
            abort(404, message=f"Does not exist {kwargs}")
        else:
            try:
                device.update(**data)
                return modbus_device_marshaller(cls.get_device(**kwargs), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if not device:
            abort(404, message=f'Not found {kwargs}')
        device.delete_from_db()
        return '', 204

    @classmethod
    def get_device(cls, **kwargs) -> ModbusDeviceModel:
        raise NotImplementedError
