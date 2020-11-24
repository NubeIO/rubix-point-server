from sqlalchemy.orm import validates

from src import db
from src.models.device.model_device_mixin import DeviceMixinModel
from src.source_drivers.modbus.models.network import ModbusType


class ModbusDeviceModel(DeviceMixinModel):
    __tablename__ = 'modbus_devices'

    type = db.Column(db.Enum(ModbusType), nullable=False)
    address = db.Column(db.Integer(), nullable=False)
    tcp_ip = db.Column(db.String(80))
    tcp_port = db.Column(db.Integer())
    zero_based = db.Column(db.Boolean(), nullable=False, default=False)
    timeout = db.Column(db.Float(), nullable=False, default=1)
    timeout_global = db.Column(db.Boolean(), nullable=False, default=True)
    # TODO: implement. used for "known working register"
    #   if can't read, device is considered "offline", break device loop
    #   else continue reading all points
    ping_point_type = db.Column(db.String(80))
    ping_point_address = db.Column(db.Integer())

    @classmethod
    def get_polymorphic_identity(cls):
        return 'Modbus'

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
