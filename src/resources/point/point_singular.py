from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.point.model_point import PointModel
from src.resources.point.point_base import PointBase
from src.resources.rest_schema.schema_point import point_all_fields, point_all_attributes
from src.models.point.priority_array import PriorityArrayModel
from src.services.points_registry import PointsRegistry


class PointSingular(PointBase):
    patch_parser = reqparse.RequestParser()
    for attr in point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(point_all_fields)
    def get(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Generic Point not found')
        return point

    @classmethod
    @marshal_with(point_all_fields)
    def put(cls, **kwargs):
        data: dict = cls.parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if point is None:
            return cls.add_point(data)
        return cls.update_point(data, point)

    @classmethod
    def update_point(cls, data: dict, point: PointModel) -> PointModel:
        priority_array_write: dict = data.pop('priority_array_write') if data.get('priority_array_write') else {}
        highest_priority_value: float = PriorityArrayModel.get_highest_priority_value_from_priority_array(
            point.priority_array_write)
        if not priority_array_write and not highest_priority_value:
            priority_array_write = {'_16': data.get('fallback_value', None) or point.fallback_value}
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
    @marshal_with(point_all_fields)
    def patch(cls, **kwargs):
        data: dict = cls.patch_parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if point is None:
            raise NotFoundException('Generic Point not found')
        return cls.update_point(data, point)

    @classmethod
    def delete(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        point.publish_cov(point.point_store, force_clear=True)
        if point is None:
            raise NotFoundException('Generic Point not found')
        point.delete_from_db()
        PointsRegistry().delete_point(point)
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        raise NotImplementedError


class PointSingularByUUID(PointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_uuid(kwargs.get('uuid'))


class PointSingularByName(PointSingular):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                       kwargs.get('point_name'))


class PointNameByUUID(RubixResource):
    @classmethod
    def get(cls, uuid):
        point: PointModel = PointModel.find_by_uuid(uuid)
        if not point:
            raise NotFoundException('Generic Point not found')
        return {'name': f'{point.device.network.name}:{point.device.name}:{point.name}'}
