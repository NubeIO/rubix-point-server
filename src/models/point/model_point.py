from sqlalchemy.orm import validates
from sqlalchemy import and_

from src import db
from src.interfaces.point import HistoryType
from src.models.model_base import ModelBase
from src.models.device.model_device import DeviceModel
from src.models.point.model_point_store import PointStoreModel
from src.event_dispatcher import EventType


class PointModel(ModelBase):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    writable = db.Column(db.Boolean, nullable=False, default=False)
    write_value = db.Column(db.Float, nullable=True, default=None)  # TODO: more data types...
    driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @staticmethod
    def check_can_add(data: dict) -> bool:
        if not DeviceModel.find_by_uuid(data.get('device_uuid')):
            raise ValueError('Device does not exist for that device_uuid')
        return True

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db()

    # TODO: use this for writing endpoint and produce COV event
    def write_point(self, uuid: str, value: float) -> bool:
        assert type(value) == float
        res = db.session.execute(self.__table__
                                     .update()
                                     .values(write_value=value)
                                     .where(and_(self.__table__.c.uuid == self.point_uuid,
                                                 self.__table__.c.writable == True)))
        return bool(res.rowcount)

    @validates('history_interval')
    def validate_history_interval(self, _, value):
        if self.history_type == HistoryType.INTERVAL and value is not None and value < 1:
            raise ValueError("history_interval needs to be at least 1, default is 15 (in minutes)")
        return value

    def get_model_event_name(self) -> str:
        return 'point'

    def get_model_event_type(self) -> EventType:
        return EventType.POINT_UPDATE
