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

    parser.add_argument('rtu_port', type=int, required=False)
    parser.add_argument('rtu_speed', type=int, required=False)
    parser.add_argument('rtu_stopbits', type=int, required=False)
    parser.add_argument('rtu_parity', type=str, required=False)
    parser.add_argument('rtu_bytesize', type=int, required=False)

    parser.add_argument('fault', type=bool, required=False)
    parser.add_argument('last_poll_timestamp', type=str, required=False)
    parser.add_argument('fault_timestamp', type=str, required=False)

    @staticmethod
    def create_network_model_obj(uuid, data):
        return ModbusNetworkModel(uuid=uuid,
                                  name=data['name'],
                                  type=data['type'],
                                  enable=data['enable'],
                                  timeout=data['timeout'],
                                  device_timeout_global=data['device_timeout_global'],
                                  point_timeout_global=data['point_timeout_global'],
                                  rtu_port=data['rtu_port'],
                                  rtu_speed=data['rtu_speed'],
                                  rtu_stopbits=data['rtu_stopbits'],
                                  rtu_parity=data['rtu_parity'],
                                  rtu_bytesize=data['rtu_bytesize'],
                                  fault=data['fault'],
                                  last_poll_timestamp=data['last_poll_timestamp'],
                                  fault_timestamp=data['fault_timestamp'])

    def add_network(self, uuid, data):
        from src.modbus.resources.network.network_plural import ModusNetworkPlural
        try:
            network = ModusNetworkPlural.create_network_model_obj(uuid, data)
            network.save_to_db()
            return network, 201
        except Exception as e:
            abort(500, message=str(e))
