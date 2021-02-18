from abc import abstractmethod

from src.source_drivers.generic.models.point import GenericPointModel
from src.source_drivers.generic.resources.point.point_singular_base import GenericPointSingularBase


class GenericPointSingularByName(GenericPointSingularBase):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericPointModel:
        return GenericPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                              kwargs.get('point_name'))
