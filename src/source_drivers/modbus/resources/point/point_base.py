from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_attributes


class ModbusPointBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        parser.add_argument(attr,
                            type=modbus_point_all_attributes[attr]['type'],
                            required=modbus_point_all_attributes[attr].get('required', False),
                            help=modbus_point_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_point_model_obj(uuid, data):
        return ModbusPointModel(uuid=uuid, **data)

    @classmethod
    def add_point(cls, data, uuid):
        try:
            point = ModbusPointBase.create_point_model_obj(uuid, data)
            point.save_to_db()
            return point
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
