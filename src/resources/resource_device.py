from flask_restful import Resource, reqparse, abort, marshal_with
from src.resources.utils import map_rest_schema
from src.models.device.model_device import DeviceModel
from src.resources.rest_schema.schema_device import device_all_attributes, \
    device_return_attributes, INTERFACE_NAME

device_all_fields = {}
map_rest_schema(device_return_attributes, device_all_fields)
map_rest_schema(device_all_attributes, device_all_fields)


class DeviceResource(Resource):
    parser = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser.add_argument(attr,
                            type=device_all_attributes[attr]['type'],
                            required=device_all_attributes[attr]['required'],
                            help=device_all_attributes[attr]['help'],
                            )

    @classmethod
    @marshal_with(device_all_fields)
    def get(cls, uuid):
        device = DeviceModel.find_by_uuid(uuid)
        if not device:
            abort(404, message=f'{INTERFACE_NAME} not found')

        return device


class DeviceResourceList(Resource):
    @classmethod
    @marshal_with(device_all_fields, envelope="devices")
    def get(cls):
        return DeviceModel.query.all()
