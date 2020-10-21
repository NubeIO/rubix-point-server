from flask_restful import abort, marshal_with

from src.modbus.interfaces.point.points import ModbusDataType, ModbusPointType, ModbusDataEndian
from src.modbus.models.point import ModbusPointModel
from src.modbus.resources.mod_fields import point_fields
from src.modbus.resources.point.point_base import ModbusPointBase


class ModbusPointSingular(ModbusPointBase):
    @marshal_with(point_fields)
    def get(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'Modbus Point not found')
        return point

    @marshal_with(point_fields)
    def put(self, uuid):
        data = ModbusPointSingular.parser.parse_args()
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            return self.add_point(data, uuid)
        else:
            self.abort_if_device_does_not_exist(data.device_uuid)
            try:
                if data.type:
                    data.type = ModbusPointType.__members__.get(data.type)
                if data.data_type:
                    data.data_type = ModbusDataType.__members__.get(data.data_type)
                if data.data_endian:
                    data.data_endian = ModbusDataEndian.__members__.get(data.data_endian)
                ModbusPointModel.filter_by_uuid(uuid).update(data)
                ModbusPointModel.commit()
                return ModbusPointModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    def delete(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204
