from sqlalchemy.orm import validates

from src import db
from src.modbus.models.network import ModbusType


class ModbusDeviceModel(db.Model):
    __tablename__ = 'mod_devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(ModbusType), nullable=False)
    addr = db.Column(db.Integer(), nullable=False)
    tcp_ip = db.Column(db.String(80))
    tcp_port = db.Column(db.Integer())
    ping_point_type = db.Column(db.String(80), nullable=False)
    ping_point_address = db.Column(db.Integer(), nullable=False)
    zero_mode = db.Column(db.Boolean(), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean())
    last_poll_timestamp = db.Column(db.DateTime)
    fault_timestamp = db.Column(db.DateTime)
    network_uuid = db.Column(db.String, db.ForeignKey('mod_networks.uuid'), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    points = db.relationship('ModbusPointModel', cascade="all,delete", backref='mod_device', lazy=True)

    def __repr__(self):
        return f"ModbusDeviceModel({self.uuid})"

    @validates('tcp_ip')
    def validate_tcp_ip(self, _, value):
        if not value and self.type == ModbusType.TCP.name:
            raise ValueError("tcp_ip should be be there on type TCP")
        return value

    @validates('tcp_port')
    def validate_tcp_port(self, _, value):
        if not value and self.type == ModbusType.TCP.name:
            raise ValueError("tcp_port should be be there on type TCP")
        return value

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
