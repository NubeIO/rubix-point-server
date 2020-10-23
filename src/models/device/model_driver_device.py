from src.models.device.model_device import DeviceModel
from src import db
from sqlalchemy.ext.declarative import declared_attr


class DriverDeviceModel(DeviceModel):
    __abstract__ = True
    DRIVER_NAME = 'DEFAULT_DRIVER_DEVICE'
    __tablename__ = 'DEFAULT_DRIVER_devices'

    @declared_attr
    def device_uuid(cls):
        return db.Column(db.String(80), db.ForeignKey('devices.device_uuid'), primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DRIVER_NAME
    }

    def __repr__(self):
        return f"DEFAULT {self.DRIVER_NAME} Device(device_uuid = {self.device_uuid})"
    #
    # @classmethod
    # def find_by_device_uuid(cls, device_uuid):
    #     return cls.query.filter_by(device_uuid=device_uuid).first()
    #
    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()
