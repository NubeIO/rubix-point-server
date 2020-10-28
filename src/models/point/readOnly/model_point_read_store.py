from src import db


class PointReadStoreModel(db.Model):
    __tablename__ = 'points_read_store'
    point_uuid = db.Column(db.String, db.ForeignKey('points.point_uuid'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"PointReadStore(point_uuid = {self.point_uuid})"
