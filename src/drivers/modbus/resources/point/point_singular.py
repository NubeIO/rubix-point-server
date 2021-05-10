from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.resources.point.point_base import ModbusPointBase
from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields, \
    modbus_point_all_attributes
from src.models.point.priority_array import PriorityArrayModel


class ModbusPointSingular(ModbusPointBase):
    """
    It returns point with point_store object value, which has the current values of point_store for that particular
    point with last not null value and value_raw
    """
    patch_parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        patch_parser.add_argument(attr,
                                  type=modbus_point_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def get(cls, **kwargs):
        point: ModbusPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Modbus Point not found')
        return point

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        point: ModbusPointModel = cls.get_point(**kwargs)
        if not point:
            return cls.add_point(data)
        return cls.update_point(data, point)

    @classmethod
    def update_point(cls, data: dict, point: ModbusPointModel) -> ModbusPointModel:
        priority_array_write: dict = data.pop('priority_array_write') if data.get('priority_array_write') else {}
        if priority_array_write:
            PriorityArrayModel.filter_by_point_uuid(point.uuid).update(priority_array_write)
        point.update(**data)
        return point

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        point: ModbusPointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException('Modbus Point not found')
        return cls.update_point(data, point)

    @classmethod
    def delete(cls, **kwargs):
        point: ModbusPointModel = cls.get_point(**kwargs)
        point.publish_cov(point.point_store, force_clear=True)
        if not point:
            raise NotFoundException('Modbus Point not found')
        point.delete_from_db()
        return '', 204

    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        raise NotImplementedError


class ModbusPointSingularByUUID(ModbusPointSingular):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_uuid(kwargs.get('uuid'))


class ModbusPointSingularByName(ModbusPointSingular):
    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        return ModbusPointModel.find_by_name(kwargs.get('network_name'), kwargs.get('device_name'),
                                             kwargs.get('point_name'))
