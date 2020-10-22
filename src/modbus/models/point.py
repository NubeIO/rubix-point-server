from src import db
from src.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian


class ModbusPointModel(db.Model):
    __tablename__ = 'mod_points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    reg = db.Column(db.Integer(), nullable=False)
    reg_length = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(ModbusPointType), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    write_value = db.Column(db.Float(), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False)
    data_round = db.Column(db.Integer(), nullable=False)
    data_offset = db.Column(db.String(80), nullable=False)
    timeout = db.Column(db.Integer(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)
    prevent_duplicates = db.Column(db.Boolean(), nullable=False)
    prevent_duplicates_global = db.Column(db.Boolean(), nullable=False)
    write_ok = db.Column(db.Boolean())
    fault = db.Column(db.Boolean())
    last_poll_timestamp = db.Column(db.DateTime)
    fault_timestamp = db.Column(db.DateTime)
    value = db.Column(db.Integer())
    value_array = db.Column(db.String())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    device_uuid = db.Column(db.String, db.ForeignKey('mod_devices.uuid'), nullable=False)

    def __repr__(self):
        return f"ModbusPointModel({self.uuid})"

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def filter_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
