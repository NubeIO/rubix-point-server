from src.drivers.enums.drivers import Drivers
from src.models.device.model_device_mixin import DeviceMixinModel


class GenericDeviceModel(DeviceMixinModel):
    __tablename__ = 'generic_devices'

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return Drivers.GENERIC.value
