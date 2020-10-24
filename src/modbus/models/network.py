from sqlalchemy.orm import validates

from src import db
from src.modbus.interfaces.network.network import ModbusType, ModbusRtuParity


class ModbusNetworkModel(db.Model):
    __tablename__ = 'mod_networks'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(ModbusType), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    device_timeout_global = db.Column(db.Float(), nullable=False)
    point_timeout_global = db.Column(db.Float(), nullable=False)
    rtu_port = db.Column(db.String(80))
    rtu_speed = db.Column(db.Integer())
    rtu_stopbits = db.Column(db.Integer())
    rtu_parity = db.Column(db.Enum(ModbusRtuParity))
    rtu_bytesize = db.Column(db.Integer(), default=8)
    fault = db.Column(db.Boolean(), nullable=True)
    last_poll_timestamp = db.Column(db.DateTime, nullable=True)
    fault_timestamp = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    devices = db.relationship('ModbusDeviceModel', cascade="all,delete", backref='mod_network', lazy=True)

    def __repr__(self):
        return f"ModbusNetworkModel({self.uuid})"

    @validates('rtu_port')
    def validate_rtu_port(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_port should be be there on type MTU")
        return value

    @validates('rtu_speed')
    def validate_rtu_speed(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_speed should be be there on rtu_speed MTU")
        return value

    @validates('rtu_stopbits')
    def validate_rtu_stopbits(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_stopbits should be be there on type MTU")
        return value

    @validates('rtu_parity')
    def validate_rtu_parity(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_parity should be be there on type MTU")
        return value

    @validates('rtu_bytesize')
    def validate_rtu_bytesize(self, _, value):
        if self.type == ModbusType.RTU.name:
            if value not in range(5, 9):
                raise ValueError("rtu_bytesize should be on range (0-9)")
            elif not value:
                raise ValueError("rtu_bytesize should be be there on type MTU")
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
