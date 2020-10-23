from sqlalchemy import join
from sqlalchemy.orm import column_property
from src import db
from src.models.point.model_point import PointModel
from src.models.point.readOnly.model_point_read_store import PointReadStoreModel


class PointModelReadOnly(db.Model):

    __table__ = join(PointModel, PointReadStoreModel)

    point_uuid = column_property(PointModel.point_uuid, PointReadStoreModel.point_uuid)

    def __repr__(self):
        return f"PointReadOnly(point_uuid = {self.point_uuid})"
