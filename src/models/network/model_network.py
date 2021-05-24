import re

from sqlalchemy.orm import validates, joinedload

from src import db
from src.drivers.enums.drivers import Drivers
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
    driver = db.Column(db.Enum(Drivers), default=Drivers.GENERIC)

    __mapper_args__ = {
        'polymorphic_identity': 'network',
        'polymorphic_on': driver
    }

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
    def find_all(cls, *args, **kwargs):
        from src.models.point.model_point import PointModel
        from src.models.device.model_device import DeviceModel
        if 'source' in kwargs:
            return db.session.query(cls) \
                .options(joinedload(cls.devices)
                         .lazyload(DeviceModel.points.and_(PointModel.source == kwargs['source']))) \
                .all()
        return super().find_all()

    @classmethod
    def find_by_uuid(cls, uuid: str, *args, **kwargs):
        from src.models.point.model_point import PointModel
        from src.models.device.model_device import DeviceModel
        if 'source' in kwargs:
            return db.session.query(cls) \
                .options(joinedload(NetworkModel.devices)
                         .lazyload(DeviceModel.points.and_(PointModel.source == kwargs['source']))) \
                .filter_by(uuid=uuid) \
                .first()
        return super().find_by_uuid(uuid)

    @classmethod
    def find_by_name(cls, network_name: str, *args, **kwargs):
        from src.models.point.model_point import PointModel
        from src.models.device.model_device import DeviceModel
        if 'source' in kwargs:
            return db.session.query(cls) \
                .options(joinedload(NetworkModel.devices)
                         .lazyload(DeviceModel.points.and_(PointModel.source == kwargs['source']))) \
                .filter_by(name=network_name) \
                .first()
        return cls.query.filter_by(name=network_name).first()

    def set_fault(self, is_fault: bool):
        self.fault = is_fault
        db.session.commit()
