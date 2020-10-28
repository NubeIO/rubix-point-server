from src import db
from src.models.point.model_point_store import PointStoreModel


class PointModel(db.Model):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    prevent_duplicates = db.Column(db.Boolean(), nullable=False)
    driver = db.Column(db.String(80))
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
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
        # self.point_store = PointStoreModel(point_uuid=self.uuid, value=0, value_array='')
        self.point_store = PointStoreModel(point_uuid=self.uuid, value=0)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def write_point_value(self, value):
    #     if self.value is None:
    #         self.value = PointStoreModel(point_uuid=self.uuid, value=value)
    #     else:
    #         self.value.value = value
