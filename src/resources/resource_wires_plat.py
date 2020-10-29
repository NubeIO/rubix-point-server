import uuid
from flask_restful import Resource, reqparse, marshal_with, abort

from src.models.wires.model_wires_plat import WiresPlatModel
from src.resources.utils import mapRestSchema

from src.resources.rest_schema.schema_wires_plat import wires_plat_all_attributes, \
    wires_plat_return_attributes

wires_plat_all_fields = {}
mapRestSchema(wires_plat_return_attributes, wires_plat_all_fields)
mapRestSchema(wires_plat_all_attributes, wires_plat_all_fields)


class WiresPlatResource(Resource):
    parser = reqparse.RequestParser()
    for attr in wires_plat_all_attributes:
        parser.add_argument(attr,
                            type=wires_plat_all_attributes[attr]['type'],
                            required=wires_plat_all_attributes[attr]['required'],
                            help=wires_plat_all_attributes[attr]['help'],
                            )

        @staticmethod
        def create_wires_model_obj(uuid, data):
            return WiresPlatModel(uuid=uuid, **data)

        @staticmethod
        def add_wires(uuid, data):
            try:
                wires = WiresPlatResource.create_wires_model_obj(uuid, data)
                wires.save_to_db()
                return wires
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def get(cls):
        wires = WiresPlatModel.query.all()
        latest = wires[-1]
        if not wires:
            abort(404, message='Wires details not found')
        return latest

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = WiresPlatResource.parser.parse_args()
        return cls.add_wires(_uuid, data)

