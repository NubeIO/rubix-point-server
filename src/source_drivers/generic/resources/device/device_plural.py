import uuid

from flask_restful.reqparse import request

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.device.device_base import GenericDeviceBase, generic_device_marshaller


class GenericDevicePlural(GenericDeviceBase):

    @classmethod
    def get(cls):
        return generic_device_marshaller(GenericDeviceModel.query.all(), request.args)

    @classmethod
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = GenericDevicePlural.parser.parse_args()
        return generic_device_marshaller(cls.add_device(_uuid, data), request.args)
