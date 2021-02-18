from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.point.point_singular_base import ModbusPointSingularBase


class ModbusPointSingularByName(ModbusPointSingularBase):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                             kwargs.get('point_name'))
