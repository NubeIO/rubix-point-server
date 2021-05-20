from flask_restful import marshal_with, reqparse

from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.resources.point.point_base import ModbusPointBase
from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields


class ModbusPointPlural(ModbusPointBase):
    @classmethod
    @marshal_with(modbus_point_all_fields)
    def get(cls):
        source_parser = reqparse.RequestParser()
        source_parser.add_argument('source', type=str, required=False, location='args', store_missing=False)
        args = source_parser.parse_args()
        source = args.get('source')
        if source is None:
            return ModbusPointModel.find_all()
        return ModbusPointModel.find_by_source(source)

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def post(cls):
        data = ModbusPointPlural.parser.parse_args()
        return cls.add_point(data)
