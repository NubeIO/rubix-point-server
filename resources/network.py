from flask_restful import Resource, reqparse
from models.network import NetworkModel


class Network(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ip',
                        type=str,
                        required=True,
                        help='ip must be a string.'
                        )
    parser.add_argument('mask',
                        type=int,
                        required=True,
                        help='netmask must be an int length 2.'
                        )
    parser.add_argument('port',
                        type=int,
                        required=True,
                        help='port must must be an int length 4.'
                        )
    parser.add_argument('network_number',
                        type=int,
                        required=True,
                        help='bacnet network number must must be an int.'
                        )

    # uuid, ip, mask, port, network_number
    def get(self, name):
        uuid = name
        network = NetworkModel.find_by_uuid(uuid)
        if network:
            return network.get_network()
        return {'message': 'Network not found'}, 404

    def post(self, name):  # add new network
        uuid = name
        if NetworkModel.find_by_uuid(uuid):
            return {'message': "An Network with uuid '{}' already exists.".format(uuid)}, 400

        data = Network.parser.parse_args()
        print(data)

        network = NetworkModel(uuid, data['ip'], data['mask'], data['port'], data['network_number'])
        try:
            network.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the network.'}, 500
        return network.get_network(), 201

    def patch(self, name):   # update a network
        uuid = name
        data = Network.parser.parse_args()
        print(data)
        network = NetworkModel.find_by_uuid(uuid)
        if network is None:
            network = NetworkModel(uuid, data['ip'], data['mask'], data['port'], data['network_number'])
        else:
            network.ip = data['ip']
            network.mask = data['mask']
            network.port = data['port']
            network.network_number = data['network_number']
        network.save_to_db()

        return network.get_network(), 201

    def delete(self, name):
        uuid = name
        network = NetworkModel.find_by_uuid(uuid)
        if network:
            network.delete_from_db()

        return {'message': 'Network deleted'}


class NetworkList(Resource):
    def get(self):
        return {'networks': [network.get_network() for network in NetworkModel.query.all()]}
