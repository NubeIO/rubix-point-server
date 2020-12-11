from flask_restful import abort, marshal_with, reqparse

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.device.device_base import GenericDeviceBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_fields, \
    generic_device_all_attributes


class GenericDeviceSingular(GenericDeviceBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_device_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_device_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_device_all_fields)
    def get(cls, uuid):
        device = GenericDeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message='Generic Device not found')
        return device

    @classmethod
    @marshal_with(generic_device_all_fields)
    def put(cls, uuid):
        data = GenericDeviceSingular.parser.parse_args()
        device = GenericDeviceModel.find_by_uuid(uuid)
        if device is None:
            return cls.add_device(uuid, data)
        else:
            try:
                device.update(**data)
                return GenericDeviceModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    @marshal_with(generic_device_all_fields)
    def patch(cls, uuid):
        data = GenericDeviceSingular.patch_parser.parse_args()
        device = GenericDeviceModel.find_by_uuid(uuid)
        if device is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                device.update(**data)
                return GenericDeviceModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        device = GenericDeviceModel.find_by_uuid(uuid)
        if device is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            device.delete_from_db()
        return '', 204
