from flask_restful import Resource, abort
from flask_restful.reqparse import request

from src.models.device.model_device import DeviceModel
from src.resources.rest_schema.schema_device import device_all_fields, device_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, device_all_fields, device_all_fields_with_children)


class DeviceResourceByUUID(Resource):
    @classmethod
    def get(cls, uuid):
        device: DeviceModel = DeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message='Device not found')
        return device_marshaller(device, request.args)


class DeviceResourceByName(Resource):
    @classmethod
    def get(cls, network_name: str, device_name: str):
        device: DeviceModel = DeviceModel.find_by_name(network_name, device_name)
        if not device:
            abort(404, message='Device not found')
        return device_marshaller(device, request.args)


class DeviceResourceList(Resource):
    @classmethod
    def get(cls):
        return device_marshaller(DeviceModel.find_all(), request.args)
