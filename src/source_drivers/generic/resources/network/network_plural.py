import uuid

from flask_restful.reqparse import request

from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.network.network_base import GenericNetworkBase, generic_network_marshaller


class GenericNetworkPlural(GenericNetworkBase):

    @classmethod
    def get(cls):
        return generic_network_marshaller(GenericNetworkModel.query.all(), request.args)

    @classmethod
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = GenericNetworkPlural.parser.parse_args()
        return generic_network_marshaller(cls.add_network(_uuid, data), request.args)
