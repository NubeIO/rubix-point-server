from flask_restful import Resource, reqparse, abort

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel


class ModbusDeviceBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('enable', type=bool, required=True)
    parser.add_argument('type', type=str, required=True)
    parser.add_argument('addr', type=int, required=True)
    parser.add_argument('tcp_ip', type=str, required=False)
    parser.add_argument('tcp_port', type=int, required=False)
    parser.add_argument('ping_point_type', type=str, required=True)
    parser.add_argument('ping_point_address', type=int, required=True)
    parser.add_argument('zero_mode', type=bool, required=True)
    parser.add_argument('timeout', type=float, required=True)
    parser.add_argument('timeout_global', type=bool, required=True)
    parser.add_argument('fault', type=bool, required=False)
    parser.add_argument('last_poll_timestamp', type=str, required=False)
    parser.add_argument('fault_timestamp', type=str, required=False)
    parser.add_argument('network_uuid', type=str, required=True)

    @staticmethod
    def create_device_model_obj(uuid, data):
        return ModbusDeviceModel(uuid=uuid, **data)

    def add_device(self, uuid, data):
        self.abort_if_network_does_not_exist_and_type_mismatch(data.network_uuid, data.type)
        try:
            device = ModbusDeviceBase.create_device_model_obj(uuid, data)
            device.save_to_db()
            return device, 201
        except Exception as e:
            abort(500, message=str(e))

    def abort_if_network_does_not_exist_and_type_mismatch(self, network_uuid, type):
        network = ModbusNetworkModel.find_by_uuid(network_uuid)
        if not network:
            abort(400, message='Network does not exist of that network_uuid')
        if network.type.name != type:
            abort(400, message=f'Type Mismatch: network.type is `{network.type}` and device.type needs to be same')
