from src import db
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian
from src.models.point.model_point_store import PointStoreModel
from src.models.point.model_driver_point import DriverPointModel


class ModbusPointModel(DriverPointModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_points'

    reg = db.Column(db.Integer(), nullable=False)
    reg_length = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(ModbusPointType), nullable=False)
    # write_value = db.Column(db.Float(), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False)
    data_round = db.Column(db.Integer(), nullable=False)
    data_offset = db.Column(db.String(80), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)
