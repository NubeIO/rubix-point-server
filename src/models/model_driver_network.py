from src.models.model_network import NetworkModel


class DriverNetworkModel(NetworkModel):
    DRIVER_NAME = 'DEFAULT_DRIVER_NETWORK'
    __tablename__ = 'DEFAULT_DRIVER_networks'

    # network_uuid = db.Column(db.String(80), db.ForeignKey('networks.network_uuid'),  primary_key=True, nullable=False)

    # __mapper_args__ = {
    #     'polymorphic_identity': DRIVER_NAME
    # }

    def __repr__(self):
        return f"{self.DRIVER_NAME} Network(network_uuid = {self.network_uuid})"
