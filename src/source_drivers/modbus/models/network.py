from sqlalchemy.orm import validates

from src import db
from src.models.network.model_network_mixin import NetworkMixinModel
from src.source_drivers import MODBUS_SERVICE_NAME
from src.source_drivers.modbus.interfaces.network.network import ModbusType, ModbusRtuParity


class ModbusNetworkModel(NetworkMixinModel):
    __tablename__ = 'modbus_networks'
    type = db.Column(db.Enum(ModbusType), nullable=False)
    rtu_port = db.Column(db.String(80), nullable=True, unique=True)
    rtu_speed = db.Column(db.Integer(), default=9600)
    rtu_stop_bits = db.Column(db.Integer(), default=1)
    rtu_parity = db.Column(db.Enum(ModbusRtuParity), default=ModbusRtuParity.N)
    rtu_byte_size = db.Column(db.Integer(), default=8)

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return MODBUS_SERVICE_NAME

    @validates('type')
    def validate_type(self, _, value):
        if isinstance(value, ModbusType):
            return value
        if not value or value not in ModbusType.__members__:
            raise ValueError("Invalid network type")
        return ModbusType[value]

    @validates('rtu_port')
    def validate_rtu_port(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_port should be be there on type MTU")
        return value

    @validates('rtu_byte_size')
    def validate_rtu_byte_size(self, _, value):
        msg = "rtu_byte_size The number of bits in a byte of serial data. This can be one of 5, 6, 7, or 8. This " \
              "defaults to 8"
        if value not in range(5, 9):
            raise ValueError(msg)
        elif not value:
            raise ValueError(msg)
        return value
