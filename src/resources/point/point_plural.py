from flask_restful import marshal_with

from src.models.point.model_point import PointModel
from src.resources.point.point_base import PointBase
from src.resources.rest_schema.schema_point import point_all_fields


class PointPlural(PointBase):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls):
        return PointModel.find_all()

    @classmethod
    @marshal_with(point_all_fields)
    def post(cls):
        data = PointPlural.parser.parse_args()
        return cls.add_point(data)
