from flask_restful import Resource, reqparse, abort

from src.models.point.model_point import PointModel


class GenericPointValueWriter(Resource):
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('value', type=float, required=True)
    patch_parser.add_argument('value_raw', type=float, required=False)
    patch_parser.add_argument('fault', type=bool, required=False)
    patch_parser.add_argument('fault_message', type=str, required=False)

    @classmethod
    def patch(cls, uuid):
        data = GenericPointValueWriter.patch_parser.parse_args()
        point: PointModel = PointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'Does not exist {uuid}')
        if not point.writable:
            abort(400, message=f'Is not writable {uuid}')
        try:
            point.update_point_store(value=data.get('value'),
                                     value_raw=data.get('value_raw') if data.get('value_raw') else data.get('value'),
                                     fault=data.get('fault'),
                                     fault_message=data.get('fault_message'))
            return {}
        except Exception as e:
            abort(501, message=str(e))
