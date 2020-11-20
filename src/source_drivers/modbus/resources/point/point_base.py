from flask_restful import Resource, reqparse, abort

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_attributes
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType


class ModbusPointBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        parser.add_argument(attr,
                            type=modbus_point_all_attributes[attr]['type'],
                            required=modbus_point_all_attributes[attr].get('required', False),
                            help=modbus_point_all_attributes[attr].get('help', None),
                            )

    @staticmethod
    def create_point_model_obj(uuid, data):
        return ModbusPointModel(uuid=uuid, **data)

    @staticmethod
    def abort_if_device_does_not_exist(device_uuid):
        if not ModbusDeviceModel.find_by_uuid(device_uuid):
            abort(400, message='Device does not exist of that device_uuid')

    @classmethod
    def add_point(cls, data, uuid):
        cls.abort_if_device_does_not_exist(data.device_uuid)
        try:
            point_type = data.get('type')
            if point_type is ModbusPointType.WRITE_COIL or point_type is ModbusPointType.WRITE_REGISTER \
                    or point_type is ModbusPointType.WRITE_COILS or point_type is ModbusPointType.WRITE_REGISTERS:
                data['writable'] = True
            point = ModbusPointBase.create_point_model_obj(uuid, data)
            point.save_to_db()
            return point
        except Exception as e:
            abort(500, message=str(e))

    @staticmethod
    def create_point_store(row):
        if row:
            return {
                'value': row.value,
                'value_array': row.value_array,
                'fault': row.fault,
                'fault_message': row.fault_message,
                'ts': str(row.ts) if row.ts else None,
            }
        else:
            return {
                'value': None,
                'value_array': None,
                'fault': None,
                'fault_message': None,
                'ts': None,
            }
