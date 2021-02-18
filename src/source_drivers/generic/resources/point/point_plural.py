from flask_restful import marshal_with

from src.source_drivers.generic.models.point import GenericPointModel
from src.source_drivers.generic.resources.point.point_base import GenericPointBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields


class GenericPointPlural(GenericPointBase):
    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls):
        points = GenericPointModel.find_all()
        return points

    @classmethod
    @marshal_with(generic_point_all_fields)
    def post(cls):
        data = GenericPointPlural.parser.parse_args()
        return cls.add_point(data)
