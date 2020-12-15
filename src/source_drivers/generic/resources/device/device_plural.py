import uuid
from flask_restful import marshal_with

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.device.device_base import GenericDeviceBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_fields


class GenericDevicePlural(GenericDeviceBase):

    @classmethod
    @marshal_with(generic_device_all_fields)
    def get(cls):
        return GenericDeviceModel.query.all()

    @classmethod
    @marshal_with(generic_device_all_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = GenericDevicePlural.parser.parse_args()
        return cls.add_device(_uuid, data)
