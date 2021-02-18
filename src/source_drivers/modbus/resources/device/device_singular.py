from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.device.device_singular_base import ModbusDeviceSingularBase


class ModbusDeviceSingular(ModbusDeviceSingularBase):
    @classmethod
    def get_device(cls, **kwargs) -> ModbusDeviceModel:
        return ModbusDeviceModel.find_by_uuid(kwargs.get('uuid'))
