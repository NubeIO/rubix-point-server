import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic.models.device import GenericDeviceModel
from src.drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_attributes, \
    generic_device_all_fields, generic_device_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def generic_device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, generic_device_all_fields,
                                          generic_device_all_fields_with_children)


class GenericDeviceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_device_all_attributes:
        parser.add_argument(attr,
                            type=generic_device_all_attributes[attr]['type'],
                            required=generic_device_all_attributes[attr].get('required', False),
                            help=generic_device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_device(cls, data):
        uuid: str = shortuuid.uuid()
        device = GenericDeviceModel(uuid=uuid, **data)
        device.save_to_db()
        return device
