from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.point.model_point import PointModel
from src.resources.rest_schema.schema_point import point_all_fields


class PointResource(RubixResource):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Point not found')
        return point

    @classmethod
    def delete(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Point not found')
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


class PointResourceList(RubixResource):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls):
        source_parser = reqparse.RequestParser()
        source_parser.add_argument('source', type=str, required=False, location='args', store_missing=False)
        args = source_parser.parse_args()
        source = args.get('source')
        if source is None:
            return PointModel.find_all()
        return PointModel.find_by_source(source)
