from flask_restful.reqparse import request

from src.models.device.model_device import DeviceModel
from src.resources.device.device_base import DeviceBase, device_marshaller


class DevicePlural(DeviceBase):

    @classmethod
    def get(cls):
        return device_marshaller(DeviceModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = DevicePlural.parser.parse_args()
        return device_marshaller(cls.add_device(data), request.args)
