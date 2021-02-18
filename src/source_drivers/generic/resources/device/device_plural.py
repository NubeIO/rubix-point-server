from flask_restful.reqparse import request

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.device.device_base import GenericDeviceBase, generic_device_marshaller


class GenericDevicePlural(GenericDeviceBase):

    @classmethod
    def get(cls):
        return generic_device_marshaller(GenericDeviceModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = GenericDevicePlural.parser.parse_args()
        return generic_device_marshaller(cls.add_device(data), request.args)
