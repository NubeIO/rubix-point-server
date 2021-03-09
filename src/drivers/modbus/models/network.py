from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.enums.network.network import ModbusType, ModbusRtuParity
from src.models.network.model_network_mixin import NetworkMixinModel


class ModbusNetworkModel(NetworkMixinModel):
    __tablename__ = 'modbus_networks'

    rtu_port = db.Column(db.String(80), nullable=True, unique=True)
    rtu_speed = db.Column(db.Integer(), default=9600)
    rtu_stop_bits = db.Column(db.Integer(), default=1)
    rtu_parity = db.Column(db.Enum(ModbusRtuParity), default=ModbusRtuParity.N)
    rtu_byte_size = db.Column(db.Integer(), default=8)
    tcp_ip = db.Column(db.String(80))
    tcp_port = db.Column(db.Integer())
    type = db.Column(db.Enum(ModbusType), nullable=False)
    timeout = db.Column(db.Integer(), nullable=False, default=3)
    polling_interval_runtime = db.Column(db.Integer(), default=2)
    point_interval_ms_between_points = db.Column(db.Integer(), default=30)

    __table_args__ = (
        UniqueConstraint('tcp_ip', 'tcp_port'),
    )

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.MODBUS

    @validates('type')
    def validate_type(self, _, value):
        if value == ModbusType.RTU.name:
            if not self.rtu_port:
                raise ValueError("rtu_port should be be there on type RTU")
            if not self.rtu_byte_size or self.rtu_byte_size not in range(5, 9):
                raise ValueError("rtu_byte_size The number of bits in a byte of serial data. This can be one of 5, 6, "
                                 "7, or 8. This defaults to 8")
        elif value == ModbusType.TCP.name:
            if not self.tcp_ip:
                raise ValueError("tcp_ip should be be there on type TCP")
            if not self.tcp_port:
                raise ValueError("tcp_port should be be there on type TCP")
        return value
