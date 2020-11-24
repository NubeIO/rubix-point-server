from sqlalchemy.orm import validates

from src import db
from src.models.network.model_network_mixin import NetworkMixinModel
from src.source_drivers.modbus.interfaces.network.network import ModbusType, ModbusRtuParity


class ModbusNetworkModel(NetworkMixinModel):
    __tablename__ = 'modbus_networks'
    type = db.Column(db.Enum(ModbusType), nullable=False)
    timeout = db.Column(db.Float(), nullable=False, default=1)
    device_timeout_global = db.Column(db.Float(), nullable=False, default=1)
    point_timeout_global = db.Column(db.Float(), nullable=False, default=1)
    rtu_port = db.Column(db.String(80), nullable=False)
    rtu_speed = db.Column(db.Integer(), default=9600)
    rtu_stop_bits = db.Column(db.Integer(), default=1)
    rtu_parity = db.Column(db.Enum(ModbusRtuParity), default=ModbusRtuParity.N)
    rtu_byte_size = db.Column(db.Integer(), default=8)

    @classmethod
    def get_polymorphic_identity(cls):
        return 'Modbus'

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

    @validates('rtu_stop_bits')
    def validate_rtu_stop_bits(self, _, value):
        msg = "rtu_stop_bits The number of bits sent after each character in a message to indicate the end of the " \
              "byte. This defaults to 1 "
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError(msg)
        return value

    @validates('rtu_parity')
    def validate_rtu_parity(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_parity should be be there on type MTU")
        return value

    @validates('rtu_byte_size')
    def validate_rtu_byte_size(self, _, value):
        msg = "rtu_byte_size The number of bits in a byte of serial data. This can be one of 5, 6, 7, or 8. This " \
              "defaults to 8"
        if self.type == ModbusType.RTU.name:
            if value not in range(5, 9):
                raise ValueError(msg)
            elif not value:
                raise ValueError(msg)
        return value
