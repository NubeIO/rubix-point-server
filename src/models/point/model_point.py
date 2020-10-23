from src import db
from src.models.point.model_point_store import PointStoreModel


class PointModel(db.Model):
    __tablename__ = 'points'
    point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    point_name = db.Column(db.String(80), nullable=False)
    point_device_uuid = db.Column(db.String, db.ForeignKey('devices.device_uuid'), nullable=False)
    point_enable = db.Column(db.Boolean(), nullable=False)
    point_fault = db.Column(db.Boolean(), nullable=True)
    point_prevent_duplicates = db.Column(db.Boolean(), nullable=False)
    point_driver = db.Column(db.String(80))
    value = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")

    __mapper_args__ = {
        'polymorphic_identity': 'point',
        'polymorphic_on': point_driver
    }

    def __repr__(self):
        return f"Point(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def write_point_value(self, value):
        if self.value is None:
            self.value = PointStoreModel(point_uuid=self.point_uuid, point_value=value)
        else:
            self.value.value = value
