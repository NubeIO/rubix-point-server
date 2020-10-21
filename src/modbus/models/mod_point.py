from src import db
from src.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian


class ModbusPointModel(db.Model):
    __tablename__ = 'mod_points'
    mod_point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_point_name = db.Column(db.String(80), nullable=False)
    mod_point_reg = db.Column(db.Integer(), nullable=False)
    mod_point_reg_length = db.Column(db.Integer(), nullable=False)
    mod_point_type = db.Column(db.Enum(ModbusPointType), nullable=False)
    mod_point_enable = db.Column(db.Boolean(), nullable=False)
    mod_point_write_value = db.Column(db.Integer(), nullable=False)
    mod_point_data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    mod_point_data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False)
    mod_point_data_round = db.Column(db.Integer(), nullable=False)
    mod_point_data_offset = db.Column(db.String(80), nullable=False)
    mod_point_timeout = db.Column(db.Integer(), nullable=False)
    mod_point_timeout_global = db.Column(db.Boolean(), nullable=False)
    mod_point_prevent_duplicates = db.Column(db.Boolean(), nullable=False)
    mod_point_prevent_duplicates_global = db.Column(db.Boolean(), nullable=False)
    mod_point_write_ok = db.Column(db.Boolean(), nullable=True)
    mod_point_fault = db.Column(db.Boolean(), nullable=True)
    mod_point_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_point_value = db.Column(db.Integer(), nullable=True)
    mod_point_value_array = db.Column(db.String(), nullable=True)
    mod_device_uuid = db.Column(db.String, db.ForeignKey('mod_devices.uuid'))

    def __repr__(self):
        return f"ModbusPointModel(mod_point_uuid = {self.mod_point_uuid})"

    @classmethod
    def find_by_uuid(cls, mod_point_uuid):
        return cls.query.filter_by(mod_point_uuid=mod_point_uuid).first()

    @classmethod
    def filter_by_uuid(cls, mod_point_uuid):
        return cls.query.filter_by(mod_point_uuid=mod_point_uuid)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
