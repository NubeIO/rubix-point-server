import enum
from sqlalchemy.orm import validates
from src import db
from src.models.network.model_driver_network import DriverNetworkModel


class ModbusType(enum.Enum):
    RTU = 0
    TCP = 1


class Parity(enum.Enum):
    O = "O"
    E = "E"
    N = "N"
    Odd = "Odd"
    Even = "Even"


class ModbusNetworkModel(DriverNetworkModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_networks'

    mod_network_type = db.Column(db.Enum(ModbusType), nullable=False)
    mod_network_timeout = db.Column(db.Integer(), nullable=False)
    mod_network_device_timeout_global = db.Column(db.Integer(), nullable=False)
    mod_network_point_timeout_global = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_port = db.Column(db.String(80), nullable=False)
    mod_rtu_network_speed = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_stopbits = db.Column(db.Integer(), nullable=False)
    mod_rtu_network_parity = db.Column(db.Enum(Parity), nullable=True)
    mod_rtu_network_bytesize = db.Column(db.Integer(), default=8)
    mod_network_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_network_fault_timestamp = db.Column(db.String(80), nullable=True)

    @validates('mod_rtu_network_bytesize')
    def validate_bytesize(self, _, bytesize):
        if bytesize not in range(5, 9):
            raise ValueError("mod_rtu_network_bytesize should be on range (0-9)")
        return bytesize
