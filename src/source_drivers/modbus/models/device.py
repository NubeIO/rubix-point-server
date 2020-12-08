from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

from src import db
from src.source_drivers.modbus.services import MODBUS_SERVICE_NAME
from src.models.network.model_network import NetworkModel
from src.models.device.model_device_mixin import DeviceMixinModel
from src.source_drivers.modbus.models.network import ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel


class ModbusDeviceModel(DeviceMixinModel):
    __tablename__ = 'modbus_devices'

    type = db.Column(db.Enum(ModbusType), nullable=False)
    address = db.Column(db.Integer(), nullable=False)
    tcp_ip = db.Column(db.String(80))
    tcp_port = db.Column(db.Integer())
    zero_based = db.Column(db.Boolean(), nullable=False, default=False)
    timeout = db.Column(db.Float(), nullable=False, default=1)
    timeout_global = db.Column(db.Boolean(), nullable=False, default=True)
    ping_point = db.Column(db.String(10))
    modbus_network_uuid_constraint = db.Column(db.String, nullable=False)

    __table_args__ = (
        UniqueConstraint('address', 'type', 'modbus_network_uuid_constraint'),
        UniqueConstraint('tcp_ip', 'type', 'modbus_network_uuid_constraint'),
    )

    @classmethod
    def get_polymorphic_identity(cls):
        return MODBUS_SERVICE_NAME

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

    @validates('ping_point')
    def validate_ping_point(self, _, value):
        if not value:
            raise ValueError("Invalid ping_point")
        ModbusPointModel.create_temporary_from_string(value)
        return value

    def check_self(self) -> (bool, any):
        super().check_self()
        if self.network_uuid is None:  # for temporary models
            return True
        network = NetworkModel.find_by_uuid(self.network_uuid)
        # can't get sqlalchemy column default to do this so this is solution
        if network is None:
            raise Exception(f'No network found with uuid {self.network_uuid}')
        self.type = network.type
        self.modbus_network_uuid_constraint = self.network_uuid
        return True
