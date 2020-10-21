import uuid
from flask_restful import marshal_with

from src.modbus.models.point import ModbusPointModel
from src.modbus.resources.mod_fields import point_fields
from src.modbus.resources.point.point_base import ModbusPointBase


class ModbusPointPlural(ModbusPointBase):
    @marshal_with(point_fields, envelope="points")
    def get(self):
        return ModbusPointModel.query.all()

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = ModbusPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)
