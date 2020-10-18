from flask_restful import Resource, reqparse, fields, marshal_with, abort
from src.models.modbus.mod_network import ModbusNetworkModel
from src.services.modbus.mod_network import ModbusNetworkService

network_fields = {
    'mod_network_uuid': fields.String,
    'mod_network_name': fields.String,
    'mod_network_ip': fields.String,
    'mod_network_port': fields.Integer,
    # 'network_device_id': fields.Integer,
    # 'network_device_name': fields.String,
    # 'network_number': fields.Integer,
}


class ModNetwork(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mod_network_name',
                        type=str,
                        required=True,
                        help='name must be a string'
                        )
    parser.add_argument('mod_network_ip',
                        type=str,
                        required=True,
                        help='network must be a string'
                        )
    parser.add_argument('mod_network_port',
                        type=int,
                        required=True,
                        help='network_ip must be a string'
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
        # return ModNetworkModel(network_uuid=network_uuid, network_ip=data['network_ip'], network_mask=data['network_mask'],
        #                     network_port=data['network_port'], network_device_id=data['network_device_id'],
        #                     network_device_name=data['network_device_name'], network_number=data['network_number'])


class ModNetworkList(Resource):
    @marshal_with(network_fields, envelope="mod_networks")
    def get(self):
        return ModbusNetworkModel.query.all()


class ModNetworksIds(Resource):
    @marshal_with({'mod_network_uuid': fields.String}, envelope="mod_networks")
    def get(self):
        return ModbusNetworkModel.query.all()
