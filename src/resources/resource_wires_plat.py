import uuid
from flask_restful import Resource, reqparse, marshal_with, abort

from src.models.wires.model_wires_plat import WiresPlatModel
from src.resources.rest_schema.schema_wires_plat import wires_plat_all_attributes, wires_plat_all_fields


class WiresPlatResource(Resource):
    parser = reqparse.RequestParser()
    for attr in wires_plat_all_attributes:
        parser.add_argument(attr,
                            type=wires_plat_all_attributes[attr]['type'],
                            required=wires_plat_all_attributes[attr].get('required', False),
                            help=wires_plat_all_attributes[attr].get('help', None),
                            )

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def get(cls):
        wires = WiresPlatModel.query.all()
        if len(wires) == 0:
            abort(404, message='Wires details not found')
        return wires[-1]

    @classmethod
    @marshal_with(wires_plat_all_fields)
    def put(cls):
        data = WiresPlatResource.parser.parse_args()
        wires = WiresPlatModel.query.all()
        try:
            if len(wires) == 0:
                _uuid = str(uuid.uuid4())
                wires = WiresPlatModel(uuid=_uuid, **data)
                wires.save_to_db()
                return wires
            else:
                _uuid = wires[-1].uuid
                WiresPlatModel.update_to_db(_uuid, data)
                return WiresPlatModel.find_by_uuid(_uuid)
        except Exception as e:
            abort(500, message=str(e))

    def delete(self):
        WiresPlatModel.delete_from_db()
        return '', 204
