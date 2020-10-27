from flask_restful import abort, marshal_with

from src.source_drivers.modbus.interfaces.point.points import ModbusDataType, ModbusPointType, ModbusDataEndian
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.mod_fields import point_fields
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils


class ModbusPointSingular(ModbusPointBase):
    """
    It returns point with point_store object value, which has the current values of point_store for that particular
    point with last not null value and value_array
    """

    @classmethod
    def get(cls, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'Modbus Point not found')
        return {**ModelUtils.row2dict(point), "point_store": ModelUtils.row2dict(point.value)}

    @classmethod
    @marshal_with(point_fields)
    def put(cls, uuid):
        data = ModbusPointSingular.parser.parse_args()
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            return cls.add_point(data, uuid)
        else:
            cls.abort_if_device_does_not_exist(data.device_uuid)
            try:
                if data.type:
                    data.type = ModbusPointType.__members__.get(data.type)
                if data.data_type:
                    data.data_type = ModbusDataType.__members__.get(data.data_type)
                if data.data_endian:
                    data.data_endian = ModbusDataEndian.__members__.get(data.data_endian)
                point.update(data)
                point.commit()
                return ModbusPointModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return ''
