from src import db
from src.models.model_base import ModelBase
from src.event_dispatcher import EventType


class NetworkModel(ModelBase):
    __tablename__ = 'networks'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)
    driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'network',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Network(uuid = {self.uuid})"

    def get_model_event_name(self) -> str:
        return 'network'

    def get_model_event_type(self) -> EventType:
        return EventType.NETWORK_UPDATE

    @staticmethod
    def check_can_add(data: dict) -> bool:
        return True
