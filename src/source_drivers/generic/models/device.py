from src.source_drivers import GENERIC_SERVICE_NAME
from src.models.device.model_device_mixin import DeviceMixinModel


class GenericDeviceModel(DeviceMixinModel):
    __tablename__ = 'generic_devices'

    @classmethod
    def get_polymorphic_identity(cls):
        return GENERIC_SERVICE_NAME
