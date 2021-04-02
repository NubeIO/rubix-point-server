from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.generic.enums.point.points import GenericPointType
from src.models.point.model_point_mixin import PointMixinModel


class GenericPointModel(PointMixinModel):
    __tablename__ = 'generic_points'

    type = db.Column(db.Enum(GenericPointType), nullable=False, default=GenericPointType.FLOAT)
    unit = db.Column(db.String, nullable=True)

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC

    def apply_point_type(self, value: float):
        generic_point = GenericPointModel.find_by_uuid(self.uuid)
        if generic_point is not None and value is not None:
            if generic_point.type == GenericPointType.STRING:
                value = None
            elif generic_point.type == GenericPointType.INT:
                value = round(value, 0)
            elif generic_point.type == GenericPointType.BOOL:
                value = float(bool(value))
        return value
