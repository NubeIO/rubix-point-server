from src import db
from src.models.point.model_driver_point import DriverPointModel
from src.models.point.readOnly.model_driver_point_readonly import DriverPointModelReadOnly
from src.models.point.writable.model_driver_point_writeable import DriverPointModelWritable


class ModbusPointModel(DriverPointModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_points'

    mod_point_reg = db.Column(db.Integer(), nullable=False)
    mod_point_reg_length = db.Column(db.Integer(), nullable=False)
    mod_point_type = db.Column(db.String(80), nullable=False)
    mod_point_data_type = db.Column(db.String(80), nullable=False)
    mod_point_data_endian = db.Column(db.String(80), nullable=False)
    mod_point_data_round = db.Column(db.Integer(), nullable=False)
    mod_point_data_offset = db.Column(db.String(80), nullable=False)
    mod_point_timeout = db.Column(db.Integer(), nullable=False)
    mod_point_timeout_global = db.Column(db.Boolean(), nullable=False)
    mod_point_prevent_duplicates_global = db.Column(db.Boolean(), nullable=False)
    mod_point_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_point_value_array = db.Column(db.String(), nullable=True)
