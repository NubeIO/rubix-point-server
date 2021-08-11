import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.models.point.model_point import PointModel
from src.resources.rest_schema.schema_point import point_all_attributes, \
    add_nested_priority_array_write
from src.models.point.priority_array import PriorityArrayModel
from src.services.points_registry import PointsRegistry


class PointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in point_all_attributes:
        parser.add_argument(attr,
                            type=point_all_attributes[attr]['type'],
                            required=point_all_attributes[attr].get('required', False),
                            help=point_all_attributes[attr].get('help', None),
                            store_missing=False)
    add_nested_priority_array_write()

    @classmethod
    def add_point(cls, data):
        uuid: str = shortuuid.uuid()
        priority_array_write: dict = data.pop('priority_array_write', {})
        priority_array_write_object: PriorityArrayModel = PriorityArrayModel. \
            create_priority_array_model(uuid, priority_array_write, data.get('fallback_value'))
        point = PointModel(
            uuid=uuid,
            priority_array_write=priority_array_write_object,
            **data
        )
        point.save_to_db()
        highest_priority_value: float = PriorityArrayModel.get_highest_priority_value_from_priority_array(
            priority_array_write_object)
        point.point_store.value_original = highest_priority_value
        point.update(**data)
        PointsRegistry().add_point(point)
        return point
