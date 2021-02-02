from src import db
from src.models.model_base import ModelBase


class PriorityArrayModel(db.Model):
    __tablename__ = 'priority_array'
    generic_uuid = db.Column(db.String, db.ForeignKey('generic_points.uuid'), primary_key=True, nullable=False)
    _1 = db.Column(db.Float(), nullable=True)
    _2 = db.Column(db.Float(), nullable=True)
    _3 = db.Column(db.Float(), nullable=True)
    _4 = db.Column(db.Float(), nullable=True)
    _5 = db.Column(db.Float(), nullable=True)
    _6 = db.Column(db.Float(), nullable=True)
    _7 = db.Column(db.Float(), nullable=True)
    _8 = db.Column(db.Float(), nullable=True)
    _9 = db.Column(db.Float(), nullable=True)
    _10 = db.Column(db.Float(), nullable=True)
    _11 = db.Column(db.Float(), nullable=True)
    _12 = db.Column(db.Float(), nullable=True)
    _13 = db.Column(db.Float(), nullable=True)
    _14 = db.Column(db.Float(), nullable=True)
    _15 = db.Column(db.Float(), nullable=True)
    _16 = db.Column(db.Float(), nullable=True)

    def __repr__(self):
        return f"PriorityArray(generic_uuid = {self.generic_uuid})"

    @classmethod
    def create_new_priority_array_model(cls, generic_uuid):
        return PriorityArrayModel(generic_uuid=generic_uuid)

    @classmethod
    def filter_by_point_uuid(cls, generic_uuid):
        return cls.query.filter_by(generic_uuid=generic_uuid)

    @classmethod
    def get_highest_priority_value(cls, generic_uuid):
        priority_array = cls.filter_by_point_uuid(generic_uuid).first()
        if priority_array:
            for i in range(1, 17):
                value = getattr(priority_array, f'_{i}')
                if value is not None:
                    return value
        return None
