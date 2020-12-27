from src.source_drivers import GENERIC_SERVICE_NAME
from src.models.network.model_network_mixin import NetworkMixinModel


class GenericNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_networks'

    @classmethod
    def get_polymorphic_identity(cls):
        return GENERIC_SERVICE_NAME
