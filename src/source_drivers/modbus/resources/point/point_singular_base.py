from flask_restful import abort, marshal_with, reqparse

from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields, \
    modbus_point_all_attributes


class ModbusPointSingularBase(ModbusPointBase):
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
            abort(404, message=f'Modbus Point not found')
        return point

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        point: ModbusPointModel = cls.get_point(**kwargs)
        if point is None:
            return cls.add_point(data)
        else:
            try:
                return point.update(**data)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    @marshal_with(modbus_point_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        point: ModbusPointModel = cls.get_point(**kwargs)
        if point is None:
            abort(404, message=f'Modbus Point not found')
        else:
            try:
                return point.update(**data)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        point: ModbusPointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message=f'Modbus Point not found')
        point.delete_from_db()
        return '', 204

    @classmethod
    def get_point(cls, **kwargs) -> ModbusPointModel:
        raise NotImplementedError
