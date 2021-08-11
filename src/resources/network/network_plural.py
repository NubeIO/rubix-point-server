from flask_restful.reqparse import request

from src.models.network.model_network import NetworkModel
from src.resources.network.network_base import NetworkBase, network_marshaller


class NetworkPlural(NetworkBase):

    @classmethod
    def get(cls):
        return network_marshaller(NetworkModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = NetworkPlural.parser.parse_args()
        return network_marshaller(cls.add_network(data), request.args)
