from flask_restful.reqparse import request

from src.drivers.generic.models.network import GenericNetworkModel
from src.drivers.generic.resources.network.network_base import GenericNetworkBase, generic_network_marshaller


class GenericNetworkPlural(GenericNetworkBase):

    @classmethod
    def get(cls):
        return generic_network_marshaller(GenericNetworkModel.find_all(**request.args), request.args)

    @classmethod
    def post(cls):
        data = GenericNetworkPlural.parser.parse_args()
        return generic_network_marshaller(cls.add_network(data), request.args)
