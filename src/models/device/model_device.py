from sqlalchemy import UniqueConstraint

from src import db
from src.models.model_base import ModelBase
from src.models.network.model_network import NetworkModel
from src.services.event_service_base import EventType


class DeviceModel(ModelBase):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_uuid = db.Column(db.String, db.ForeignKey('networks.uuid'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.String(80), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)
    driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'device',
        'polymorphic_on': driver
    }

    __table_args__ = (
        UniqueConstraint('name', 'network_uuid'),
    )

    def __repr__(self):
        return f"Device(device_uuid = {self.device_uuid})"

    @classmethod
    def find_by_name(cls, network_name: str, device_name: str):
        results = cls.query.filter_by(name=device_name) \
            .join(NetworkModel).filter_by(name=network_name) \
            .first()
        return results

    def get_model_event_name(self) -> str:
        return 'device'

    def get_model_event_type(self) -> EventType:
        return EventType.DEVICE_UPDATE

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
