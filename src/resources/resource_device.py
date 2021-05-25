from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.device.model_device import DeviceModel
from src.resources.rest_schema.schema_device import device_all_fields, device_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, device_all_fields, device_all_fields_with_children)


class DeviceResourceByUUID(RubixResource):
    @classmethod
    def get(cls, uuid):
        device: DeviceModel = DeviceModel.find_by_uuid(uuid, **request.args)
        if not device:
            raise NotFoundException('Device not found')
        return device_marshaller(device, request.args)


class DeviceResourceByName(RubixResource):
    @classmethod
    def get(cls, network_name: str, device_name: str):
        device: DeviceModel = DeviceModel.find_by_name(network_name, device_name, **request.args)
        if not device:
            raise NotFoundException('Device not found')
        return device_marshaller(device, request.args)


class DeviceResourceList(RubixResource):
    @classmethod
    def get(cls):
        return device_marshaller(DeviceModel.find_all(**request.args), request.args)
