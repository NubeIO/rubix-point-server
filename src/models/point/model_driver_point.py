from src.models.point.model_point import PointModel
from src import db
from sqlalchemy.ext.declarative import declared_attr


class DriverPointModel(PointModel):
    __abstract__ = True
    DRIVER_NAME = 'DEFAULT_DRIVER_POINT'
    __tablename__ = 'DEFAULT_DRIVER_points'

    @declared_attr
    def uuid(cls):
        return db.Column(db.String(80), db.ForeignKey('points.uuid'), primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DRIVER_NAME
    }

    def __repr__(self):
        return f"{self.DRIVER_NAME} Point(uuid = {self.uuid})"
