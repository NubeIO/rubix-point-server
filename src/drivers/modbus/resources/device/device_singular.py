from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.resources.device.device_base import ModbusDeviceBase, modbus_device_marshaller
from src.drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes


class ModbusDeviceSingular(ModbusDeviceBase):
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
            raise NotFoundException('Modbus Device not found')
        return modbus_device_marshaller(device, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if device is None:
            return modbus_device_marshaller(cls.add_device(data), request.args)

        device.update(**data)
        return modbus_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if device is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        device.update(**data)
        return modbus_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def delete(cls, **kwargs):
        device: ModbusDeviceModel = cls.get_device(**kwargs)
        if not device:
            raise NotFoundException(f'Not found {kwargs}')
        device.delete_from_db()
        return '', 204

    @classmethod
    def get_device(cls, **kwargs) -> ModbusDeviceModel:
        raise NotImplementedError


class ModbusDeviceSingularByUUID(ModbusDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> ModbusDeviceModel:
        return ModbusDeviceModel.find_by_uuid(kwargs.get('uuid'), **request.args)


class ModbusDeviceSingularByName(ModbusDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> ModbusDeviceModel:
        return ModbusDeviceModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'), **request.args)
