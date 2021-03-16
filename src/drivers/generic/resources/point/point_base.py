import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic.models.point import GenericPointModel
from src.drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_attributes
from src.models.point.priority_array import PriorityArrayModel
from src.services.points_registry import PointsRegistry


class GenericPointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_point_all_attributes:
        parser.add_argument(attr,
                            type=generic_point_all_attributes[attr]['type'],
                            required=generic_point_all_attributes[attr].get('required', False),
                            help=generic_point_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_point(cls, data):
        _uuid: str = str(uuid.uuid4())
        point: GenericPointModel = GenericPointModel(uuid=_uuid, **data)
        point.priority_array_write = PriorityArrayModel.create_new_priority_array_model(_uuid)
        point.save_to_db()
        PointsRegistry().add_point(point)
        return point
