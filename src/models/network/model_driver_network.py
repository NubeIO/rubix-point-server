from src.models.network.model_network import NetworkModel
from src import db
from sqlalchemy.ext.declarative import declared_attr


class DriverNetworkModel(NetworkModel):
    __abstract__ = True
    DRIVER_NAME = 'DEFAULT_DRIVER_NETWORK'
    __tablename__ = 'DEFAULT_DRIVER_networks'

    @declared_attr
    def network_uuid(cls):
        return db.Column(db.String(80), db.ForeignKey('networks.network_uuid'),  primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DRIVER_NAME
    }

    def __repr__(self):
        return f"{self.DRIVER_NAME} Network(network_uuid = {self.network_uuid})"
