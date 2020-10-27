from flask_restful import Resource, reqparse, abort

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.point import ModbusPointModel


class ModbusPointBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('reg', type=int, required=True)
    parser.add_argument('reg_length', type=int, required=True)
    parser.add_argument('type', type=str, required=True)
    parser.add_argument('enable', type=bool, required=True)
    parser.add_argument('write_value', type=float, required=True)
    parser.add_argument('data_type', type=str, required=True)
    parser.add_argument('data_endian', type=str, required=True)
    parser.add_argument('data_round', type=int, required=True)
    parser.add_argument('data_offset', type=str, required=True)
    parser.add_argument('timeout', type=float, required=True)
    parser.add_argument('timeout_global', type=bool, required=True)
    parser.add_argument('prevent_duplicates', type=bool, required=True)
    parser.add_argument('prevent_duplicates_global', type=bool, required=True)
    parser.add_argument('device_uuid', type=str, required=True)

    @staticmethod
    def create_point_model_obj(uuid, data):
        return ModbusPointModel(uuid=uuid, **data)

    def add_point(self, data, uuid):
        self.abort_if_device_does_not_exist(data.device_uuid)
        try:
            point = ModbusPointBase.create_point_model_obj(uuid, data)
            point.save_to_db()
            return point
        except Exception as e:
            abort(500, message=str(e))

    def abort_if_device_does_not_exist(self, device_uuid):
        if not ModbusDeviceModel.find_by_uuid(device_uuid):
            abort(400, message='Device does not exist of that device_uuid')

    def create_point_store(self, row):
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
