from abc import abstractmethod

from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.models.point.model_point import PointModel


class PointValueWriterBase(RubixResource):
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('value', type=float, required=False)
    patch_parser.add_argument('priority', type=int, required=False)
    patch_parser.add_argument('priority_array_write', type=dict, required=False)

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        raise NotImplementedError('Please override get_point method')

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Point does not exist')
        if not point.writable:
            raise BadDataException('Point is not writable')
        point.update_point_store(value=data.get('value'),
                                 priority=data.get('priority'),
                                 priority_array_write=data.get('priority_array_write'))
        return {}


class PointUUIDValueWriter(PointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_uuid(kwargs.get('uuid'))


class PointNameValueWriter(PointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                       kwargs.get('point_name'))
