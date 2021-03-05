from src.models.device.model_device_mixin import DeviceMixinModel
from src.source_drivers.drivers import Drivers


class GenericDeviceModel(DeviceMixinModel):
    __tablename__ = 'generic_devices'

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return Drivers.GENERIC.value
