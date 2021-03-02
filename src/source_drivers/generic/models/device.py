from src.models.device.model_device_mixin import DeviceMixinModel
from src.source_drivers import GENERIC_SERVICE_NAME


class GenericDeviceModel(DeviceMixinModel):
    __tablename__ = 'generic_devices'

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return GENERIC_SERVICE_NAME
