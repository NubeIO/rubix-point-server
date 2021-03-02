from src.models.network.model_network_mixin import NetworkMixinModel
from src.source_drivers import GENERIC_SERVICE_NAME


class GenericNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_networks'

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return GENERIC_SERVICE_NAME
