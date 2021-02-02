from src import db
from src.source_drivers import GENERIC_SERVICE_NAME
from src.models.point.model_point_mixin import PointMixinModel


class GenericPointModel(PointMixinModel):
    __tablename__ = 'generic_points'

    priority_array = db.relationship('PriorityArrayModel', backref='generic_points', lazy=False, uselist=False,
                                     cascade="all,delete")

    @classmethod
    def get_polymorphic_identity(cls):
        return GENERIC_SERVICE_NAME
