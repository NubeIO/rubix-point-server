import re

from sqlalchemy.orm import validates

from src import db
from src.models.model_base import ModelBase
from src.utils.model_utils import validate_json


class NetworkModel(ModelBase):
    __tablename__ = 'networks'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    tags = db.Column(db.String(320), nullable=True)
    devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)

    @validates('tags')
    def validate_tags(self, _, value):
        """
        Rules for tags:
        - force all tags to be lower case
        - if there is a gap add an underscore
        - no special characters
        """
        if value is not None:
            try:
                return validate_json(value)
            except ValueError:
                raise ValueError('tags needs to be a valid JSON')
        return value

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

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
