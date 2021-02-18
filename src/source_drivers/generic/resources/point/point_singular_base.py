from abc import abstractmethod

from flask_restful import abort, marshal_with, reqparse

from src.source_drivers.generic.models.point import GenericPointModel
from src.source_drivers.generic.resources.point.point_base import GenericPointBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields, \
    generic_point_all_attributes


class GenericPointSingularBase(GenericPointBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls, **kwargs):
        point: GenericPointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message=f'Generic Point not found')
        return point

    @classmethod
    @marshal_with(generic_point_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        point: GenericPointModel = cls.get_point(**kwargs)
        if point is None:
            return cls.add_point(data)
        try:
            return point.update(**data)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    @marshal_with(generic_point_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        point: GenericPointModel = cls.get_point(**kwargs)
        if point is None:
            abort(404, message=f'Generic Point not found')
        try:
            return point.update(**data)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        point: GenericPointModel = cls.get_point(**kwargs)
        if point is None:
            abort(404, message=f'Generic Point not found')
        point.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericPointModel:
        raise NotImplementedError
