import enum
from sqlalchemy.orm import validates

from src import db

attributes = {
    'mod_network_uuid': 'mod_network_uuid',
    'mod_network_name': 'mod_network_name',
    'mod_network_type': 'mod_network_type',  # rtu or tcp
    'mod_network_enable': 'mod_network_enable',
    'mod_network_timeout': 'mod_network_timeout',  # network time out
    'mod_network_device_timeout_global': 'mod_network_device_timeout_global',  # device time out global setting
    'mod_network_point_timeout_global': 'mod_network_point_timeout_global',  # point time out global setting
    'mod_rtu_network_port': 'mod_rtu_network_port',  # /dev/ttyyUSB0
    'mod_rtu_network_speed': 'mod_rtu_network_speed',  # 9600
    'mod_rtu_network_stopbits': 'mod_rtu_network_stopbits',  # 1
    'mod_rtu_network_parity': 'mod_rtu_network_parity',  # O E N Odd, Even, None
    'mod_rtu_network_bytesize': 'mod_rtu_network_bytesize',  # 5, 6, 7, or 8. This defaults to 8.
    'mod_network_fault': 'mod_network_fault',  # true
    'mod_network_last_poll_timestamp': 'mod_network_last_poll_timestamp',
    'mod_network_fault_timestamp': 'mod_network_fault_timestamp',
}


class ModbusType(enum.Enum):
    RTU = 0
    TCP = 1


class Parity(enum.Enum):
    O = "O"
    E = "E"
    N = "N"
    Odd = "Odd"
    Even = "Even"


class ModbusNetworkModel(db.Model):
    __tablename__ = 'mod_networks'
    mod_network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_network_name = db.Column(db.String(80), nullable=False)
    mod_network_type = db.Column(db.Enum(ModbusType), nullable=False)
    mod_network_enable = db.Column(db.Boolean(), nullable=False)
    mod_network_timeout = db.Column(db.Integer(), nullable=False)
    mod_network_device_timeout_global = db.Column(db.Integer(), nullable=False)
    mod_network_point_timeout_global = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_port = db.Column(db.String(80), nullable=False)
    mod_rtu_network_speed = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_stopbits = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_parity = db.Column(db.Enum(Parity), nullable=True)
    mod_rtu_network_bytesize = db.Column(db.Integer(), default=8)
    mod_network_fault = db.Column(db.Boolean(), nullable=True)
    mod_network_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_network_fault_timestamp = db.Column(db.String(80), nullable=True)
    mod_devices = db.relationship('ModbusDeviceModel', cascade="all,delete", backref='mod_network', lazy=True)

    def __repr__(self):
        return f"Network(mod_network_uuid = {self.mod_network_uuid})"

    @validates('mod_rtu_network_bytesize')
    def validate_email(self, _, bytesize):
        if bytesize not in range(5, 9):
            raise ValueError("mod_rtu_network_bytesize should be on range (0-9)")
        return bytesize

    @classmethod
    def find_by_network_uuid(cls, mod_network_uuid):
        return cls.query.filter_by(mod_network_uuid=mod_network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
