from sqlalchemy.orm import validates

from src import db
from src.source_drivers.modbus.interfaces.network.network import ModbusType, ModbusRtuParity
from src.models.network.model_driver_network import DriverNetworkModel


class ModbusNetworkModel(DriverNetworkModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_networks'

    type = db.Column(db.Enum(ModbusType), nullable=False)
    timeout = db.Column(db.Float(), nullable=False)
    device_timeout_global = db.Column(db.Float(), nullable=False)
    point_timeout_global = db.Column(db.Float(), nullable=False)
    rtu_port = db.Column(db.String(80))
    rtu_speed = db.Column(db.Integer())
    rtu_stop_bits = db.Column(db.Integer())
    rtu_parity = db.Column(db.Enum(ModbusRtuParity))
    rtu_byte_size = db.Column(db.Integer(), default=8)
    last_poll_timestamp = db.Column(db.DateTime, nullable=True)
    fault_timestamp = db.Column(db.DateTime, nullable=True)

    # TODO: move to parent
    # created_on = db.Column(db.DateTime, server_default=db.func.now())
    # updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

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
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_stop_bits should be be there on type MTU")
        return value

    @validates('rtu_parity')
    def validate_rtu_parity(self, _, value):
        if not value and self.type == ModbusType.RTU.name:
            raise ValueError("rtu_parity should be be there on type MTU")
        return value

    @validates('rtu_byte_size')
    def validate_rtu_byte_size(self, _, value):
        if self.type == ModbusType.RTU.name:
            if value not in range(5, 9):
                raise ValueError("rtu_byte_size should be on range (0-9)")
            elif not value:
                raise ValueError("rtu_byte_size should be be there on type MTU")
        return value
