import re

from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.enums.model import ModelEvent
from src.models.model_base import ModelBase
from src.services.event_service_base import EventType


class NetworkModel(ModelBase):
    __tablename__ = 'networks'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)
    driver = db.Column(db.Enum(Drivers), default=Drivers.GENERIC)

    __mapper_args__ = {
        'polymorphic_identity': 'network',
        'polymorphic_on': driver
    }

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    def __repr__(self):
        return f"Network(uuid = {self.uuid})"

    @classmethod
    def find_by_name(cls, network_name: str):
        results = cls.query.filter_by(name=network_name).first()
        return results

    def get_model_event(self) -> ModelEvent:
        return ModelEvent.NETWORK

    def get_model_event_type(self) -> EventType:
        return EventType.NETWORK_UPDATE

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
