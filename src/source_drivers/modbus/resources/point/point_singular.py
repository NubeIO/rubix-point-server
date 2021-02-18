from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.point.point_singular_base import ModbusPointSingularBase


class ModbusPointSingular(ModbusPointSingularBase):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_uuid(kwargs.get('uuid'))
