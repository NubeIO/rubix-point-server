import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.models.device.model_device import DeviceModel
from src.resources.rest_schema.schema_device import device_all_attributes, device_all_fields, \
    device_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, device_all_fields,
                                          device_all_fields_with_children)


class DeviceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser.add_argument(attr,
                            type=device_all_attributes[attr]['type'],
                            required=device_all_attributes[attr].get('required', False),
                            help=device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_device(cls, data):
        uuid: str = shortuuid.uuid()
        device = DeviceModel(uuid=uuid, **data)
        device.save_to_db()
        return device
