from src import db
from src.models.model_base import ModelBase
from src.models.network.model_network import NetworkModel
from src.event_dispatcher import EventType


class DeviceModel(ModelBase):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_uuid = db.Column(db.String, db.ForeignKey('networks.uuid'), nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    enable = db.Column(db.String(80), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)
    driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'device',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Device(device_uuid = {self.device_uuid})"

    def get_model_event_name(self) -> str:
        return 'device'

    def get_model_event_type(self) -> EventType:
        return EventType.DEVICE_UPDATE

    @staticmethod
    def check_can_add(data: dict) -> bool:
        if not NetworkModel.find_by_uuid(data.get('network_uuid')):
            raise ValueError('Network does not exist for that network_uuid')
        return True
