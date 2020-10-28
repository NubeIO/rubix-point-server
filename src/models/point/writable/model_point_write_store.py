from src import db


class PointWriteStoreModel(db.Model):
    __tablename__ = 'points_write_store'
    point_uuid = db.Column(db.String, db.ForeignKey('points.point_uuid'), primary_key=True, nullable=False)
    point_write_pending = db.Column(db.Boolean, nullable=False)
    point_write_fault = db.Column(db.Boolean, nullable=False, default=False)
    # point = db.relationship('PointModel', lazy=True, uselist=False, cascade="all,delete")

    def __repr__(self):
        return f"PointWriteStore(point_uuid = {self.point_uuid})"
