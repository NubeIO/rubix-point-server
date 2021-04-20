from abc import abstractmethod

from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.drivers.modbus.models.point import ModbusPointModel


class ModbusPointValueWriterBase(RubixResource):
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('value', type=float, required=False)
    patch_parser.add_argument('priority', type=int, required=False)

    @classmethod
    @abstractmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        raise NotImplementedError('Please override get_point method')

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        point: ModbusPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Modbus Point not found')
        if not point.writable:
            raise BadDataException('Point is not writable')
        point.update_priority_value(value=data.get('value'),
                                    priority=data.get('priority'))
        return {}


class ModbusPointUUIDValueWriter(ModbusPointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_uuid(kwargs.get('uuid'))


class ModbusPointNameValueWriter(ModbusPointValueWriterBase):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                             kwargs.get('point_name'))
