from src import db
from src.drivers.enums.droplet_type import DropletType
from src.enums.model import ModelEvent
from src.models.model_base import ModelBase
from src.services.event_service_base import EventType


class GenericNetworkDropletModel(ModelBase):
    __tablename__ = 'generic_networks_droplets'

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.Column(db.Enum(DropletType), default=DropletType.CLOUD)
    networks = db.relationship('GenericNetworkModel', cascade="all,delete", backref='device', lazy=True)

    # TODO: CURD like API for site> device
    # site_uuid = db.Column(db.String, db.ForeignKey('site.uuid'), nullable=True)
    # device_uuid = db.Column(db.String, db.ForeignKey('device.uuid'), nullable=True)

    @classmethod
    def find_by_name(cls, network_droplet_name: str):
        result = cls.query.filter_by(name=network_droplet_name).first()
        return result

    def get_model_event(self) -> ModelEvent:
        return ModelEvent.NETWORK_DROPLET

    def get_model_event_type(self) -> EventType:
        return EventType.NETWORK_DROPLET_MODEL
