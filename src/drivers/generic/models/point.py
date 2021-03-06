from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.generic.enums.point.points import GenericPointType
from src.models.point.model_point_mixin import PointMixinModel


class GenericPointModel(PointMixinModel):
    __tablename__ = 'generic_points'

    priority_array_write = db.relationship('PriorityArrayModel', backref='generic_points', lazy=False, uselist=False,
                                           cascade="all,delete")
    type = db.Column(db.Enum(GenericPointType), nullable=False, default=GenericPointType.FLOAT)
    unit = db.Column(db.String, nullable=True)

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC
