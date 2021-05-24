from flask_restful import marshal_with
from flask_restful.reqparse import request

from src.drivers.generic.models.point import GenericPointModel
from src.drivers.generic.resources.point.point_base import GenericPointBase
from src.drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields


class GenericPointPlural(GenericPointBase):
    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls):
        return GenericPointModel.find_all(**request.args)

    @classmethod
    @marshal_with(generic_point_all_fields)
    def post(cls):
        data = GenericPointPlural.parser.parse_args()
        return cls.add_point(data)
