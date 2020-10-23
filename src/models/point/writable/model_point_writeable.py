from sqlalchemy import join
from sqlalchemy.orm import column_property
from src import db
from src.models.point.model_point import PointModel
from src.models.point.writable.model_point_write_store import PointWriteStoreModel


class PointModelWritable(db.Model):

    __table__ = join(PointModel, PointWriteStoreModel)

    point_uuid = column_property(PointModel.point_uuid, PointWriteStoreModel.point_uuid)

    def __repr__(self):
        return f"PointWritable(point_uuid = {self.point_uuid})"
