from src import db


class PointStoreHistoryModel(db.Model):
    __tablename__ = 'point_stores_history'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), nullable=False)
    value = db.Column(db.Float(), nullable=True)
    value_raw = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"PointStoreHistory(point_uuid = {self.point_uuid})"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        db.session.add(self)

    @classmethod
    def get_all_after(cls, _id):
        return cls.query.filter(cls.id > _id).all()

    @classmethod
    def get_latest(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).order_by(cls.__table__.c.ts.desc()).first()
