from abc import abstractmethod

from flask_restful import abort, reqparse
from flask_restful.reqparse import request

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.device.device_base import GenericDeviceBase, generic_device_marshaller
from src.source_drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_attributes


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
            abort(404, message='Generic Device not found')
        return generic_device_marshaller(device, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            return generic_device_marshaller(cls.add_device(data), request.args)
        try:
            device.update(**data)
            return generic_device_marshaller(cls.get_device(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            abort(404, message=f"Does not exist {kwargs}")
        try:
            device.update(**data)
            return generic_device_marshaller(cls.get_device(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        device: GenericDeviceModel = cls.get_device(**kwargs)
        if device is None:
            abort(404, message=f"Does not exist {kwargs}")
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
