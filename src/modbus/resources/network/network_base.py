from flask_restful import Resource, abort, reqparse

from src.modbus.models.network import ModbusNetworkModel


class ModusNetworkBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('type', type=str, required=True)
    parser.add_argument('enable', type=bool, required=True)
    parser.add_argument('timeout', type=int, required=True)
    parser.add_argument('device_timeout_global', type=int)
    parser.add_argument('point_timeout_global', type=int)

    parser.add_argument('rtu_port', type=str, required=False) # dev/ttyUSB0
    parser.add_argument('rtu_speed', type=int, required=False) # 9600
    parser.add_argument('rtu_stopbits', type=int, required=False)
    parser.add_argument('rtu_parity', type=str, required=False)
    parser.add_argument('rtu_bytesize', type=int, required=False)

    parser.add_argument('fault', type=bool, required=False)
    parser.add_argument('last_poll_timestamp', type=str, required=False)
    parser.add_argument('fault_timestamp', type=str, required=False)

    @staticmethod
    def create_network_model_obj(uuid, data):
        return ModbusNetworkModel(uuid=uuid, **data)

    def add_network(self, uuid, data):
        try:
            network = ModusNetworkBase.create_network_model_obj(uuid, data)
            network.save_to_db()
            return network, 201
        except Exception as e:
            abort(500, message=str(e))
