from flask_restful import Resource, reqparse, abort, marshal_with

from src.models.point.model_point import PointModel
# from src.models.point.writable.model_point_writeable import PointModelWritable
# from src.models.point.readOnly.model_point_readonly import PointModelReadOnly
from src.resources.rest_schema.schema_point import point_all_attributes, point_return_attributes, INTERFACE_NAME
from src.resources.utils import *

point_all_fields = {}
map_rest_schema(point_return_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)


class PointResource(Resource):
    parser = reqparse.RequestParser()
    for attr in point_all_attributes:
        parser.add_argument(attr,
                            type=point_all_attributes[attr]['type'],
                            required=point_all_attributes[attr]['required'],
                            help=point_all_attributes[attr]['help'],
                            )

    @classmethod
    @marshal_with(point_all_fields)
    def get(cls, uuid):
        point = PointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'{INTERFACE_NAME} not found')
        return point

    @classmethod
    def delete(cls, uuid):
        point = PointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204


class PointResourceList(Resource):
    @classmethod
    @marshal_with(point_all_fields, envelope="points")
    def get(cls):
        result = PointModel.query.all()
        return result

# class PointWriteableResourceList(Resource):
#     @classmethod
#     @marshal_with(point_all_fields, envelope="points_writable")
#     def get(cls):
#         result = PointModelWritable.query.all()
#         return result
#
#
# class PointReadOnlyResourceList(Resource):
#     @classmethod
#     @marshal_with(point_all_fields, envelope="points_readOnly")
#     def get(cls):
#         result = PointModelReadOnly.query.all()
#         return result
