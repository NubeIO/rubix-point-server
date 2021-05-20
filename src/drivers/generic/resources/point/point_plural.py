from flask_restful import marshal_with, reqparse

from src.drivers.generic.models.point import GenericPointModel
from src.drivers.generic.resources.point.point_base import GenericPointBase
from src.drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields


class GenericPointPlural(GenericPointBase):
    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls):
        source_parser = reqparse.RequestParser()
        source_parser.add_argument('source', type=str, required=False, location='args', store_missing=False)
        args = source_parser.parse_args()
        source = args.get('source')
        if source is None:
            return GenericPointModel.find_all()
        return GenericPointModel.find_by_source(source)

    @classmethod
    @marshal_with(generic_point_all_fields)
    def post(cls):
        data = GenericPointPlural.parser.parse_args()
        return cls.add_point(data)
