from src import db
from src.models.point.model_point_store import PointStoreModelMixin


class PointStoreHistoryModel(PointStoreModelMixin, db.Model):
    __tablename__ = 'point_stores_history'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), nullable=False)

    def __repr__(self):
        return f"PointStoreHistory(point_uuid = {self.point_uuid})"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        db.session.add(self)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_after(cls, _id):
        return cls.query.filter(cls.id > _id).all()

    @classmethod
    def get_latest(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).order_by(cls.__table__.c.ts.desc()).first()
