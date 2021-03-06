from sqlalchemy.ext.declarative import declared_attr

from src import db
from src.drivers.enums.drivers import Drivers
from src.models.point.model_point import PointModel


class PointMixinModel(PointModel):
    __abstract__ = True

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        pass

    @declared_attr
    def uuid(self):
        return db.Column(db.String(80), db.ForeignKey('points.uuid'), primary_key=True, nullable=False)

    @declared_attr
    def __mapper_args__(self):
        return {
            'polymorphic_identity': self.get_polymorphic_identity()
        }

    def __repr__(self):
        return f"{self.get_polymorphic_identity().value}Point(uuid = {self.uuid})"
