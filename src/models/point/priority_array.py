from sqlalchemy import inspect

from src import db
from src.utils import dbsession


class PriorityArrayModel(db.Model):
    __tablename__ = 'priority_array'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)
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
        return f"PriorityArray(uuid = {self.point_uuid})"

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def delete_from_db(self):
        db.session.delete(self)
        dbsession.commit(db)

    def update_with_no_commit(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.check_self()

    def update(self, **kwargs):
        highest_priority_value: float = self.update_with_no_commit(**kwargs)
        dbsession.commit(db)
        return highest_priority_value

    def check_self(self) -> float:
        highest_priority_value: float = self.get_highest_priority_value_from_priority_array(self)
        if highest_priority_value is None:
            from src.models.point.model_point import PointModel
            point: PointModel = self.point
            self._16 = point.fallback_value
            highest_priority_value = point.fallback_value
        return highest_priority_value

    @classmethod
    def create_priority_array_model(cls, point_uuid, priority_array_write, fallback_value):
        priority_array = PriorityArrayModel(point_uuid=point_uuid, **priority_array_write)
        if cls.get_highest_priority_value_from_priority_array(priority_array) is None:
            priority_array._16 = fallback_value
        return priority_array

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def get_highest_priority_value(cls, point_uuid):
        priority_array: PriorityArrayModel = cls.find_by_point_uuid(point_uuid)
        return cls.get_highest_priority_value_from_priority_array(priority_array)

    @classmethod
    def get_highest_priority_value_from_priority_array(cls, priority_array):
        if priority_array:
            for i in range(1, 17):
                value = getattr(priority_array, f'_{i}', None)
                if value is not None:
                    return value
        return None
