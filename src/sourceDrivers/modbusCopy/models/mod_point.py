from src import db
from src.models.model_driver_point import DriverPointModel


class ModbusPointModel(DriverPointModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_points'
    point_uuid = db.Column(db.String(80), db.ForeignKey('points.point_uuid'), primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DRIVER_NAME
    }
    mod_point_reg = db.Column(db.Integer(), nullable=False)
    mod_point_reg_length = db.Column(db.Integer(), nullable=False)
    mod_point_type = db.Column(db.String(80), nullable=False)
    mod_point_write_value = db.Column(db.Integer(), nullable=False)
    mod_point_data_type = db.Column(db.String(80), nullable=False)
    mod_point_data_endian = db.Column(db.String(80), nullable=False)
    mod_point_data_round = db.Column(db.Integer(), nullable=False)
    mod_point_data_offset = db.Column(db.String(80), nullable=False)
    mod_point_timeout = db.Column(db.Integer(), nullable=False)
    mod_point_timeout_global = db.Column(db.Boolean(), nullable=False)
    mod_point_prevent_duplicates_global = db.Column(db.Boolean(), nullable=False)
    mod_point_write_ok = db.Column(db.Boolean(), nullable=True)
    mod_point_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_point_value = db.Column(db.Integer(), nullable=True)
    mod_point_value_array = db.Column(db.String(), nullable=True)
