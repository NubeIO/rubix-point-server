from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.source_drivers.generic.models.point import GenericPointModel
from src.source_drivers.generic.models.priority_array import PriorityArrayModel
from src.source_drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_attributes


class GenericPointBase(Resource):
    parser = reqparse.RequestParser()
    for attr in generic_point_all_attributes:
        parser.add_argument(attr,
                            type=generic_point_all_attributes[attr]['type'],
                            required=generic_point_all_attributes[attr].get('required', False),
                            help=generic_point_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_point(cls, data, uuid):
        try:
            point = GenericPointModel(uuid=uuid, **data)
            point.priority_array = PriorityArrayModel.create_new_priority_array_model(uuid)
            point.save_to_db()
            return point
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
