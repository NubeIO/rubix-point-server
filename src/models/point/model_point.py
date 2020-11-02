from src import db
from src.interfaces.point import HistoryType
from src.models.point.model_point_store import PointStoreModel


class PointModel(db.Model):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.COV)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    driver = db.Column(db.String(80))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @classmethod
    def find_by_uuid(cls, point_uuid):
        return cls.query.filter_by(uuid=point_uuid).first()

    def save_to_db(self):
        self.point_store = PointStoreModel(point_uuid=self.uuid, value=0)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
