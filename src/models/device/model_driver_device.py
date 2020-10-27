from src.models.device.model_device import DeviceModel
from src import db
from sqlalchemy.ext.declarative import declared_attr


class DriverDeviceModel(DeviceModel):
    __abstract__ = True
    DRIVER_NAME = 'DEFAULT_DRIVER_DEVICE'
    __tablename__ = 'DEFAULT_DRIVER_devices'

    @declared_attr
    def uuid(cls):
        return db.Column(db.String(80), db.ForeignKey('devices.uuid'), primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DRIVER_NAME
    }

    def __repr__(self):
        return f"DEFAULT {self.DRIVER_NAME} Device(uuid = {self.uuid})"
