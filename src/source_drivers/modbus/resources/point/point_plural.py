from flask_restful import marshal_with

from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields


class ModbusPointPlural(ModbusPointBase):
    @classmethod
    @marshal_with(modbus_point_all_fields)
    def get(cls):
        points = ModbusPointModel.find_all()
        return points

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def post(cls):
        data = ModbusPointPlural.parser.parse_args()
        return cls.add_point(data)
