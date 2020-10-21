from src import db
from src.modbus.models.network import ModbusType


class ModbusDeviceModel(db.Model):
    __tablename__ = 'mod_devices'
    mod_device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_device_name = db.Column(db.String(80), nullable=False)
    mod_device_enable = db.Column(db.String(80), nullable=False)
    mod_device_type = db.Column(db.Enum(ModbusType), nullable=False)
    mod_device_addr = db.Column(db.Integer(), nullable=False)
    mod_tcp_device_ip = db.Column(db.String(80), nullable=False)
    mod_tcp_device_port = db.Column(db.Integer(), nullable=False)
    mod_ping_point_type = db.Column(db.String(80), nullable=False)
    mod_ping_point_address = db.Column(db.Integer(), nullable=False)
    mod_device_zero_mode = db.Column(db.Boolean(), nullable=False)
    mod_device_timeout = db.Column(db.Integer(), nullable=False)
    mod_device_timeout_global = db.Column(db.Boolean(), nullable=False)
    mod_device_fault = db.Column(db.Boolean(), nullable=True)
    mod_device_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_device_fault_timestamp = db.Column(db.String(80), nullable=True)
    mod_network_uuid = db.Column(db.String, db.ForeignKey('mod_networks.uuid'))
    mod_points = db.relationship('ModbusPointModel', cascade="all,delete", backref='mod_device', lazy=True)

    def __repr__(self):
        return f"ModbusDeviceModel(mod_device_uuid = {self.mod_device_uuid})"

    @classmethod
    def find_by_device_uuid(cls, mod_device_uuid):
        return cls.query.filter_by(mod_device_uuid=mod_device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
