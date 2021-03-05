from src.models.network.model_network_mixin import NetworkMixinModel
from src.source_drivers.drivers import Drivers


class GenericNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_networks'

    @classmethod
    def get_polymorphic_identity(cls) -> str:
        return Drivers.GENERIC.value
