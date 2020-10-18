from flask_restful import Resource, reqparse, fields, marshal_with, abort
from src.models.modbus.mod_network import ModbusNetworkModel
from src.services.modbus.mod_network import ModbusNetworkService
from src.interfaces.modbus.network.interface_modbus_network import THIS, \
    interface_mod_network_name, interface_mod_network_type, \
    interface_mod_network_enable, interface_mod_network_timeout, \
    interface_mod_network_device_timeout_global, interface_mod_network_point_timeout_global, \
    interface_mod_rtu_network_port, interface_mod_rtu_network_speed, \
    interface_mod_rtu_network_stopbits, interface_mod_rtu_network_parity, \
    interface_mod_rtu_network_bytesize

network_fields = {
    'mod_network_uuid': fields.String,
    'mod_network_name': fields.String,
    'mod_network_type': fields.String,  # rtu or tcp
    'mod_network_enable': fields.Boolean,
    'mod_network_timeout': fields.Integer,  # network time out
    'mod_network_device_timeout_global': fields.Integer,  # device time out global setting
    'mod_network_point_timeout_global': fields.Integer,  # point time out global setting
    'mod_rtu_network_port': fields.String,  # /dev/ttyyUSB0
    'mod_rtu_network_speed': fields.Integer,  # 9600
    'mod_rtu_network_stopbits': fields.Integer,  # 1
    'mod_rtu_network_parity': fields.String,  # O E N Odd, Even, None
    'mod_rtu_network_bytesize': fields.Integer  # 5, 6, 7, or 8. This defaults to 8.
}



class ModNetwork(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(interface_mod_network_name['name'],
                        type=interface_mod_network_name['type'],
                        required=interface_mod_network_name['required'],
                        help=interface_mod_network_name['help'],
                        )
    parser.add_argument(interface_mod_network_type['name'],
                        type=interface_mod_network_type['type'],
                        required=interface_mod_network_type['required'],
                        help=interface_mod_network_type['help'],
                        )
    parser.add_argument(interface_mod_network_enable['name'],
                        type=interface_mod_network_enable['type'],
                        required=interface_mod_network_enable['required'],
                        help=interface_mod_network_enable['help'],
                        )
    parser.add_argument(interface_mod_network_timeout['name'],
                        type=interface_mod_network_timeout['type'],
                        required=interface_mod_network_timeout['required'],
                        help=interface_mod_network_timeout['help'],
                        )
    parser.add_argument(interface_mod_network_device_timeout_global['name'],
                        type=interface_mod_network_device_timeout_global['type'],
                        required=interface_mod_network_device_timeout_global['required'],
                        help=interface_mod_network_device_timeout_global['help'],
                        )
    parser.add_argument(interface_mod_network_point_timeout_global['name'],
                        type=interface_mod_network_point_timeout_global['type'],
                        required=interface_mod_network_point_timeout_global['required'],
                        help=interface_mod_network_point_timeout_global['help'],
                        )
    parser.add_argument(interface_mod_rtu_network_port['name'],
                        type=interface_mod_rtu_network_port['type'],
                        required=interface_mod_rtu_network_port['required'],
                        help=interface_mod_rtu_network_port['help'],
                        )
    parser.add_argument(interface_mod_rtu_network_speed['name'],
                        type=interface_mod_rtu_network_speed['type'],
                        required=interface_mod_rtu_network_speed['required'],
                        help=interface_mod_rtu_network_speed['help'],
                        )
    parser.add_argument(interface_mod_rtu_network_stopbits['name'],
                        type=interface_mod_rtu_network_stopbits['type'],
                        required=interface_mod_rtu_network_stopbits['required'],
                        help=interface_mod_rtu_network_stopbits['help'],
                        )
    parser.add_argument(interface_mod_rtu_network_parity['name'],
                        type=interface_mod_rtu_network_parity['type'],
                        required=interface_mod_rtu_network_parity['required'],
                        help=interface_mod_rtu_network_parity['help'],
                        )
    parser.add_argument(interface_mod_rtu_network_bytesize['name'],
                        type=interface_mod_rtu_network_bytesize['type'],
                        required=interface_mod_rtu_network_bytesize['required'],
                        help=interface_mod_rtu_network_bytesize['help'],
                        )

    @marshal_with(network_fields)
    def get(self, uuid):
        network = ModbusNetworkModel.find_by_network_uuid(uuid)
        if not network:
            abort(404, message='Modbus Network not found')
        return network

    @marshal_with(network_fields)
    def post(self, uuid):
        if ModbusNetworkModel.find_by_network_uuid(uuid):
            return abort(409, message=f"An Modbus Network with network_uuid '{uuid}' already exists.")
        data = ModNetwork.parser.parse_args()
        network = ModNetwork.create_network_model_obj(uuid, data)
        network.save_to_db()
        ModbusNetworkService.get_instance().add_network(network)
        return network, 201

    @marshal_with(network_fields)
    def put(self, uuid):
        data = ModNetwork.parser.parse_args()
        network = ModbusNetworkModel.find_by_network_uuid(uuid)
        if network is None:
            network = ModNetwork.create_network_model_obj(uuid, data)
        else:
            network.mod_network_name = data['mod_network_name']
            network.mod_network_ip = data['mod_network_ip']
            network.mod_network_port = data['mod_network_port']
            # network.network_number = data['network_number']
            # network.network_device_id = data['network_device_id']
            # network.network_device_name = data['network_device_name']
        network.save_to_db()
        ModbusNetworkService.get_instance().add_network(network)
        return network, 201

    def delete(self, uuid):
        mod_network_uuid = uuid
        network = ModbusNetworkModel.find_by_network_uuid(mod_network_uuid)
        if network:
            network.delete_from_db()
            ModbusNetworkService.get_instance().delete_network(network)
        return '', 204

    @staticmethod
    def create_network_model_obj(mod_network_uuid, data):
        return ModbusNetworkModel(mod_network_uuid=mod_network_uuid, mod_network_name=data['mod_network_name'], mod_network_ip=data['mod_network_ip'], mod_network_port=data['mod_network_port'])



class ModNetworkList(Resource):
    @marshal_with(network_fields, envelope="mod_networks")
    def get(self):
        return ModbusNetworkModel.query.all()


class ModNetworksIds(Resource):
    @marshal_with({'mod_network_uuid': fields.String}, envelope="mod_networks")
    def get(self):
        return ModbusNetworkModel.query.all()
