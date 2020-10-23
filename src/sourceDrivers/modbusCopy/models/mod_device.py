from src import db
from src.sourceDrivers.modbusCopy.models.mod_network import ModbusType
from src.models.device.model_driver_device import DriverDeviceModel


class ModbusDeviceModel(DriverDeviceModel):
    DRIVER_NAME = 'Modbus'
    __tablename__ = 'modbus_devices'

    mod_device_type = db.Column(db.Enum(ModbusType), nullable=False)
    mod_device_addr = db.Column(db.Integer(), nullable=False)
    mod_tcp_device_ip = db.Column(db.String(80), nullable=False)
    mod_tcp_device_port = db.Column(db.Integer(), nullable=False)
    mod_ping_point_type = db.Column(db.String(80), nullable=False)
    mod_ping_point_address = db.Column(db.Integer(), nullable=False)
    mod_device_zero_mode = db.Column(db.Boolean(), nullable=False)
    mod_device_timeout = db.Column(db.Integer(), nullable=False)
    mod_device_timeout_global = db.Column(db.Boolean(), nullable=False)
    mod_device_last_poll_timestamp = db.Column(db.String(80), nullable=True)
    mod_device_fault_timestamp = db.Column(db.String(80), nullable=True)
