from src import db
from src.drivers.enums.drivers import Drivers
from src.models.network.model_network_mixin import NetworkMixinModel


class GenericNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_networks'
    droplet_uuid = db.Column(db.String, db.ForeignKey('generic_networks_droplets.uuid'), nullable=False)

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC
