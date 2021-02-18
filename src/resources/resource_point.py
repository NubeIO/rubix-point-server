from abc import abstractmethod

from flask_restful import Resource, abort, marshal_with

from src.models.point.model_point import PointModel
from src.resources.rest_schema.schema_point import point_all_fields


class PointResource(Resource):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message='Point not found')
        return point

    @classmethod
    def delete(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message='Point not found')
        point.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        raise NotImplementedError


class PointResourceByUUID(PointResource):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_uuid(kwargs.get('uuid'))


class PointResourceByName(PointResource):
    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'), kwargs.get('point_name'))


class PointResourceList(Resource):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls):
        result = PointModel.find_all()
        return result
