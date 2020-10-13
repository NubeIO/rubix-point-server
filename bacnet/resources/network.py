from flask_restful import Resource, reqparse
from bacnet.models.network import NetworkModel


class Network(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('network_ip',
                        type=str,
                        required=True,
                        help='network_ip must be a string.'
                        )
    parser.add_argument('network_mask',
                        type=int,
                        required=True,
                        help='netmask must be an int length 2.'
                        )
    parser.add_argument('network_port',
                        type=int,
                        required=True,
                        help='network_port must must be an int length 4.'
                        )
    parser.add_argument('network_number',
                        type=int,
                        required=True,
                        help='bacnet network number must must be an int.'
                        )
    parser.add_argument('network_device_id',
                        type=int,
                        required=True,
                        help='bacnet id is needed'
                        )
    parser.add_argument('network_device_name',
                        type=str,
                        required=True,
                        help='bacnet device name is needed.'
                        )

    # network_uuid, network_ip, network_mask, network_port, network_number
    def get(self, uuid):
        network_uuid = uuid
        network = NetworkModel.find_by_network_uuid(network_uuid)
        if network:
            return network.get_network()
        return {'message': 'Network not found'}, 404

    def post(self, uuid):  # add new network
        network_uuid = uuid
        if NetworkModel.find_by_network_uuid(network_uuid):
            return {'message': "An Network with network_uuid '{}' already exists.".format(network_uuid)}, 400

        data = Network.parser.parse_args()
        print(data)

        network = NetworkModel(network_uuid, data['network_ip'], data['network_mask'], data['network_port'],
                               data['network_number'], data['network_device_id'], data['network_device_name'])
        try:
            network.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the network.'}, 500
        return network.get_network(), 201

    def patch(self, uuid):  # update a network
        network_uuid = uuid
        data = Network.parser.parse_args()
        print(data)
        network = NetworkModel.find_by_network_uuid(network_uuid)
        print(network)
        if network is None:
            network = NetworkModel(network_uuid, data['network_ip'], data['network_mask'], data['network_port'],
                                   data['network_number'], data['network_device_id'], data['network_device_name'])
        else:
            network.network_ip = data['network_ip']
            network.network_mask = data['network_mask']
            network.network_port = data['network_port']
            network.network_number = data['network_number']
            network.network_device_id = data['network_device_id']
            network.network_device_name = data['network_device_name']
        network.save_to_db()

        return network.get_network(), 201

    def delete(self, uuid):
        network_uuid = uuid
        network = NetworkModel.find_by_network_uuid(network_uuid)
        if network:
            network.delete_from_db()

        return {'message': 'Network deleted'}


class NetworkList(Resource):
    def get(self):
        return {'networks': [network.get_network() for network in NetworkModel.query.all()]}


class NetworksIds(Resource):
    def get(self):
        return {'networks': [network.get_network_ids() for network in NetworkModel.query.all()]}
