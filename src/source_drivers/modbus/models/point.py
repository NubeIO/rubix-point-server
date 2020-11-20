from src import db

from src.models.point.model_point_mixin import PointMixinModel
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian


class ModbusPointModel(PointMixinModel):
    __tablename__ = 'modbus_points'

    reg = db.Column(db.Integer(), nullable=False)
    reg_length = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(ModbusPointType), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False)
    data_round = db.Column(db.Integer(), nullable=False)
    data_offset = db.Column(db.String(80), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)

    @classmethod
    def get_polymorphic_identity(cls):
        return "Modbus"
