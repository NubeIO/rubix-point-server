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
    def get(cls, uuid):
        device = GenericDeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message='Generic Device not found')
        return generic_device_marshaller(device, request.args)

    @classmethod
    def put(cls, uuid):
        data = GenericDeviceSingular.parser.parse_args()
        device = GenericDeviceModel.find_by_uuid(uuid)
        if device is None:
            return generic_device_marshaller(cls.add_device(uuid, data), request.args)
        else:
            try:
                device.update(**data)
                return generic_device_marshaller(GenericDeviceModel.find_by_uuid(uuid), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def patch(cls, uuid):
        data = GenericDeviceSingular.patch_parser.parse_args()
        device = GenericDeviceModel.find_by_uuid(uuid)
        if device is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                device.update(**data)
                return generic_device_marshaller(GenericDeviceModel.find_by_uuid(uuid), request.args)
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
