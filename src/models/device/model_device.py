import re

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.models.model_base import ModelBase
from src.models.network.model_network import NetworkModel


class DeviceModel(ModelBase):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_uuid = db.Column(db.String, db.ForeignKey('networks.uuid'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)
    driver = db.Column(db.Enum(Drivers), default=Drivers.GENERIC)

    __mapper_args__ = {
        'polymorphic_identity': 'device',
        'polymorphic_on': driver
    }

    __table_args__ = (
        UniqueConstraint('name', 'network_uuid'),
    )

    def __repr__(self):
        return f"Device(uuid = {self.uuid})"

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    @classmethod
    def find_by_name(cls, network_name: str, device_name: str):
        results = cls.query.filter_by(name=device_name) \
            .join(NetworkModel).filter_by(name=network_name) \
            .first()
        return results

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
