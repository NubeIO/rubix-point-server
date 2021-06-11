from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic.models.point import GenericPointModel
from src.drivers.generic.resources.point.point_base import GenericPointBase
from src.drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields, \
    generic_point_all_attributes
from src.models.point.priority_array import PriorityArrayModel
from src.services.points_registry import PointsRegistry


class GenericPointSingular(GenericPointBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_point_all_fields)
    def get(cls, **kwargs):
        point: GenericPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Generic Point not found')
        return point

    @classmethod
    @marshal_with(generic_point_all_fields)
    def put(cls, **kwargs):
        data: dict = cls.parser.parse_args()
        point: GenericPointModel = cls.get_point(**kwargs)
        if point is None:
            return cls.add_point(data)
        return cls.update_point(data, point)

    @classmethod
    def update_point(cls, data: dict, point: GenericPointModel) -> GenericPointModel:
        priority_array_write: dict = data.pop('priority_array_write') if data.get('priority_array_write') else {}
        if priority_array_write:
            updated_priority_array_write: PriorityArrayModel = PriorityArrayModel.find_by_point_uuid(point.uuid)
            updated_priority_array_write.update(**priority_array_write)
            highest_priority_value: float = PriorityArrayModel.get_highest_priority_value_from_priority_array(
                updated_priority_array_write)
            point.point_store.value_original = highest_priority_value
        if priority_array_write or data:
            changed: bool = point.update(**data)
            if changed:
                PointsRegistry().update_point(point)
        return point

    @classmethod
    @marshal_with(generic_point_all_fields)
    def patch(cls, **kwargs):
        data: dict = cls.patch_parser.parse_args()
        point: GenericPointModel = cls.get_point(**kwargs)
        if point is None:
            raise NotFoundException('Generic Point not found')
        return cls.update_point(data, point)

    @classmethod
    def delete(cls, **kwargs):
        point: GenericPointModel = cls.get_point(**kwargs)
        point.publish_cov(point.point_store, force_clear=True)
        if point is None:
            raise NotFoundException('Generic Point not found')
        point.delete_from_db()
        PointsRegistry().delete_point(point)
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericPointModel:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_priority_array_write(cls, **kwargs) -> PriorityArrayModel:
        raise NotImplementedError


class GenericPointSingularByUUID(GenericPointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericPointModel:
        return GenericPointModel.find_by_uuid(kwargs.get('uuid'))

    @classmethod
    @abstractmethod
    def get_priority_array_write(cls, **kwargs) -> PriorityArrayModel:
        return PriorityArrayModel.find_by_point_uuid(kwargs.get('uuid'))


class GenericPointSingularByName(GenericPointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> GenericPointModel:
        return GenericPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                              kwargs.get('point_name'))

    @classmethod
    @abstractmethod
    def get_priority_array_write(cls, **kwargs) -> PriorityArrayModel:
        return GenericPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                              kwargs.get('point_name')).priority_array_write
