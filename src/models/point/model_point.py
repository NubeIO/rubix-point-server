from sqlalchemy import and_
from sqlalchemy.orm import validates

from src import db
from src.interfaces.point import HistoryType, MathOperation
from src.models.model_base import ModelBase
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventType


class PointModel(ModelBase):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    writable = db.Column(db.Boolean, nullable=False, default=False)
    write_value = db.Column(db.Float, nullable=True, default=None)  # TODO: more data types...
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    value_round = db.Column(db.Integer(), nullable=False, default=2)
    value_offset = db.Column(db.Float(), nullable=False, default=0)
    value_operation = db.Column(db.Enum(MathOperation), nullable=True)
    input_min = db.Column(db.Float())
    input_max = db.Column(db.Float())
    scale_min = db.Column(db.Float())
    scale_max = db.Column(db.Float())
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    point_store_history = db.relationship('PointStoreHistoryModel', backref='point')
    driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

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

    def update(self, **kwargs):
        super().update(**kwargs)

        point_store = PointStoreModel.find_by_point_uuid(self.uuid)
        updated = point_store.update(self, 0)
        self.point_store = point_store
        if updated:
            point_store.publish_cov(self)

        return self
