from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.source_drivers.generic.models.device import GenericDeviceModel
from src.source_drivers.generic.resources.rest_schema.schema_generic_device import generic_device_all_attributes


class GenericDeviceBase(Resource):
    parser = reqparse.RequestParser()
    for attr in generic_device_all_attributes:
        parser.add_argument(attr,
                            type=generic_device_all_attributes[attr]['type'],
                            required=generic_device_all_attributes[attr].get('required', False),
                            help=generic_device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_device_model_obj(uuid, data):
        return GenericDeviceModel(uuid=uuid, **data)

    @classmethod
    def add_device(cls, uuid, data):
        try:
            device = GenericDeviceBase.create_device_model_obj(uuid, data)
            device.save_to_db()
            return device
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
