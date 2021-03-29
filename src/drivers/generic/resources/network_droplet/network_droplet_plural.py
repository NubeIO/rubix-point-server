from flask_restful.reqparse import request

from src.drivers.generic.models.network_droplet import GenericNetworkDropletModel
from src.drivers.generic.resources.network_droplet.network_droplet_base import GenericNetworkDropletBase, \
    generic_network_droplet_marshaller


class GenericNetworkDropletPlural(GenericNetworkDropletBase):

    @classmethod
    def get(cls):
        return generic_network_droplet_marshaller(GenericNetworkDropletModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = GenericNetworkDropletPlural.parser.parse_args()
        return generic_network_droplet_marshaller(cls.add_network_droplet(data), request.args)
