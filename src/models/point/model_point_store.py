from src import db


class PointStoreModel(db.Model):
    __tablename__ = 'points_store'
    point_uuid = db.Column(db.String, db.ForeignKey('points.point_uuid'), primary_key=True, nullable=False)
    point_value = db.Column(db.Float(), nullable=True)

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"
