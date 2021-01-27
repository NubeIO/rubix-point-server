from sqlalchemy.ext.declarative import declared_attr

from src import db
from src.models.device.model_device import DeviceModel


class DeviceMixinModel(DeviceModel):
    __abstract__ = True

    @classmethod
    def get_polymorphic_identity(cls):
        pass

    @declared_attr
    def uuid(self):
        return db.Column(db.String(80), db.ForeignKey('devices.uuid'), primary_key=True, nullable=False)

    @declared_attr
    def __mapper_args__(self):
        return {
            'polymorphic_identity': self.get_polymorphic_identity()
        }

    def __repr__(self):
        return f"{self.get_polymorphic_identity()}Device(uuid = {self.uuid})"
