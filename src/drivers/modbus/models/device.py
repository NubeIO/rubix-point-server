from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.enums.network.network import ModbusType
from src.drivers.modbus.models.point import ModbusPointModel
from src.models.device.model_device_mixin import DeviceMixinModel
from src.models.network.model_network import NetworkModel


class ModbusDeviceModel(DeviceMixinModel):
    __tablename__ = 'modbus_devices'

    type = db.Column(db.Enum(ModbusType), nullable=False)
    address = db.Column(db.Integer(), nullable=False)
    zero_based = db.Column(db.Boolean(), nullable=False, default=False)
    ping_point = db.Column(db.String(10))
    supports_multiple_rw = db.Column(db.Boolean(), nullable=False, default=True)
    modbus_network_uuid_constraint = db.Column(db.String, nullable=False)

    __table_args__ = (
        UniqueConstraint('address', 'modbus_network_uuid_constraint'),
    )

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.MODBUS

    @validates('ping_point')
    def validate_ping_point(self, _, value):
        if value is None:
            return value
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
