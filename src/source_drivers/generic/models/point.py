from src import db
from src.models.point.model_point_mixin import PointMixinModel
from src.source_drivers import GENERIC_SERVICE_NAME
from src.source_drivers.generic.interfaces.point.points import GenericPointType


class GenericPointModel(PointMixinModel):
    __tablename__ = 'generic_points'

    priority_array_write = db.relationship('PriorityArrayModel', backref='generic_points', lazy=False, uselist=False,
                                           cascade="all,delete")
    type = db.Column(db.Enum(GenericPointType), nullable=False, default=GenericPointType.FLOAT)
    unit = db.Column(db.String, nullable=True)

    @classmethod
    def get_polymorphic_identity(cls):
        return GENERIC_SERVICE_NAME
