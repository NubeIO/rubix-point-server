from src import db
from src.models.model_point import PointModel


class DriverPointModel(PointModel):
    DRIVER_NAME = 'DEFAULT_DRIVER_POINT'
    __tablename__ = 'DEFAULT_DRIVER_points'
    # point_uuid = db.Column(db.String(80), db.ForeignKey('points.point_uuid'), primary_key=True, nullable=False)
    #
    # __mapper_args__ = {
    #     'polymorphic_identity': DRIVER_NAME
    # }

    def __repr__(self):
        return f"{self.DRIVER_NAME} Point(point_uuid = {self.point_uuid})"
    #
    # @classmethod
    # def find_by_uuid(cls, point_uuid):
    #     return cls.query.filter_by(point_uuid=point_uuid).first()
    #
    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()
