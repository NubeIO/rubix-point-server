from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.network.network_singular_base import GenericNetworkSingularBase


class GenericNetworkSingularByName(GenericNetworkSingularBase):
    @classmethod
    def get_network(cls, **kwargs) -> GenericNetworkModel:
        return GenericNetworkModel.find_by_name(kwargs.get('name'))
