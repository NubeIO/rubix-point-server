from src import db

from src.models.point.model_point_mixin import PointMixinModel
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian


class ModbusPointModel(PointMixinModel):
    __tablename__ = 'modbus_points'

    reg = db.Column(db.Integer(), nullable=False)
    reg_length = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(ModbusPointType), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False, default=ModbusDataEndian.BEB_LEW)
    data_round = db.Column(db.Integer(), nullable=False, default=2)  # TODO: not used
    data_offset = db.Column(db.String(80), nullable=False, default=0)  # TODO: not used
    timeout = db.Column(db.Float(), nullable=False, default=1)  # TODO: not used
    timeout_global = db.Column(db.Boolean(), nullable=False, default=True)  # TODO: not used

    @classmethod
    def get_polymorphic_identity(cls):
        return "Modbus"
