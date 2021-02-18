from abc import abstractmethod

from flask_restful import Resource, reqparse, abort
from flask_restful.reqparse import request
from mrb.validator import is_bridge

from src.models.point.model_point import PointModel


class GenericPointValueWriterBase(Resource):
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('value', type=float, required=False)
    patch_parser.add_argument('value_raw', type=str, required=False)
    patch_parser.add_argument('fault', type=bool, required=False)
    patch_parser.add_argument('fault_message', type=str, required=False)
    patch_parser.add_argument('priority', type=int, required=False)

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> PointModel:
        raise NotImplementedError('Please override get_point method')

    @classmethod
    def patch(cls, **kwargs):
        data = GenericPointValueWriterBase.patch_parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message=f'Point does not exist')
        if not point.writable:
            abort(400, message=f'Point is not writable')
        try:
            point.update_point_store(value=data.get('value'),
                                     priority=data.get('priority'),
                                     value_raw=data.get('value_raw'),
                                     fault=data.get('fault'),
                                     fault_message=data.get('fault_message'),
                                     sync=not is_bridge(request.args))
            return {}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(501, message=str(e))


class GenericUUIDPointValueWriter(GenericPointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_uuid(kwargs.get('uuid'))


class GenericNamePointValueWriter(GenericPointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'), kwargs.get('point_name'))
