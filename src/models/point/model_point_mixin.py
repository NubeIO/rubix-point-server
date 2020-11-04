from sqlalchemy.ext.declarative import declared_attr

from src import db
from src.models.point.model_point import PointModel


class PointMixinModel(PointModel):
    __abstract__ = True

    @classmethod
    def get_polymorphic_identity(cls):
        pass

    @declared_attr
    def uuid(cls):
        return db.Column(db.String(80), db.ForeignKey('points.uuid'), primary_key=True, nullable=False)

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.get_polymorphic_identity()
        }

    def __repr__(self):
        return f"{self.get_polymorphic_identity()}Point(uuid = {self.uuid})"
