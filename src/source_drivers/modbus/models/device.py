from sqlalchemy.orm import validates

from src import db
from src.source_drivers.modbus.models.network import ModbusType
from src.models.device.model_driver_device import DriverDeviceModel


class ModbusDeviceModel(DriverDeviceModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_devices'

    type = db.Column(db.Enum(ModbusType), nullable=False)
    address = db.Column(db.Integer(), nullable=False)
    tcp_ip = db.Column(db.String(80))
    tcp_port = db.Column(db.Integer())
    ping_point_type = db.Column(db.String(80), nullable=False)
    ping_point_address = db.Column(db.Integer(), nullable=False)
    zero_mode = db.Column(db.Boolean(), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    timeout_global = db.Column(db.Boolean(), nullable=False)
    last_poll_timestamp = db.Column(db.DateTime)
    fault_timestamp = db.Column(db.DateTime)

    # TODO: move to parent
    # created_on = db.Column(db.DateTime, server_default=db.func.now())
    # updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

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
