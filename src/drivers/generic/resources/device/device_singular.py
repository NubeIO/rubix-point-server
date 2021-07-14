from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic.models.device import GenericDeviceModel
from src.drivers.generic.resources.device.device_base import GenericDeviceBase, generic_device_marshaller
from src.drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_attributes


class GenericDeviceSingular(GenericDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_device_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_device_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if not device:
            raise NotFoundException('Generic Device not found')
        return generic_device_marshaller(device, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            return generic_device_marshaller(cls.add_device(data), request.args)
        device.update(**data)
        return generic_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        device.update(**data)
        return generic_device_marshaller(cls.get_device(**kwargs), request.args)

    @classmethod
    def delete(cls, **kwargs):
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        device.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_device(cls, **kwargs) -> GenericDeviceModel:
        raise NotImplementedError


class GenericDeviceSingularByUUID(GenericDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> GenericDeviceModel:
        return GenericDeviceModel.find_by_uuid(kwargs.get('uuid'))


class GenericDeviceSingularByName(GenericDeviceSingular):
    @classmethod
    def get_device(cls, **kwargs) -> GenericDeviceModel:
        return GenericDeviceModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'))
