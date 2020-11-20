from sqlalchemy.orm import validates
from sqlalchemy import and_

from src import db
from src.interfaces.point import HistoryType
from src.models.model_base import ModelBase
from src.models.point.model_point_store import PointStoreModel


class PointModel(ModelBase):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    writable = db.Column(db.Boolean, nullable=False, default=False)
    write_value = db.Column(db.Float, nullable=True, default=None)  # TODO: more data types...
    driver = db.Column(db.String(80))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        db.session.add(self)
        db.session.commit()

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
