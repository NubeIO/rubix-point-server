from flask_restful import abort, marshal_with, reqparse

from src.source_drivers.generic.models.point import GenericPointModel
from src.source_drivers.generic.resources.point.point_base import GenericPointBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields, \
    generic_point_all_attributes


class GenericPointSingular(GenericPointBase):

    patch_parser = reqparse.RequestParser()
    for attr in generic_point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls, uuid):
        point = GenericPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'Generic Point not found')
        return point

    @classmethod
    @marshal_with(generic_point_all_fields)
    def put(cls, uuid):
        data = GenericPointSingular.parser.parse_args()
        point = GenericPointModel.find_by_uuid(uuid)
        if point is None:
            return cls.add_point(data, uuid)
        else:
            try:
                return point.update(**data)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    @marshal_with(generic_point_all_fields)
    def patch(cls, uuid):
        data = GenericPointSingular.patch_parser.parse_args()
        point = GenericPointModel.find_by_uuid(uuid)
        if point is None:
            abort(404, message=f'Generic Point not found')
        else:
            try:
                return point.update(**data)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        point = GenericPointModel.find_by_uuid(uuid)
        if point is None:
            abort(404, message=f'Generic Point not found')
        else:
            point.delete_from_db()
        return '', 204
