from abc import abstractmethod

from flask_restful import Resource, reqparse, abort
from flask_restful.reqparse import request
from mrb.validator import is_bridge

from src.models.point.model_point import PointModel


class GenericPointValueWriterBase(Resource):
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('value_raw', type=str, required=False)
    patch_parser.add_argument('fault', type=bool, required=False)
    patch_parser.add_argument('fault_message', type=str, required=False)
    patch_parser.add_argument('priority_array', type=dict, required=False)

    nested_priority_array_patch_parser = reqparse.RequestParser()
    nested_priority_array_patch_parser.add_argument('_1', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_2', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_3', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_4', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_5', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_6', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_7', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_8', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_9', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_10', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_11', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_12', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_13', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_14', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_15', type=float, location=('priority_array',))
    nested_priority_array_patch_parser.add_argument('_16', type=float, location=('priority_array',))

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
            point.update_point_store(value_raw=data.get('value_raw'),
                                     fault=data.get('fault'),
                                     fault_message=data.get('fault_message'),
                                     priority_array=data.get('priority_array'),
                                     sync=not is_bridge(request.args))
            return {}
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
