from sqlalchemy.orm import validates
from src import db


class ModelBase(db.Model):
    __abstract__ = True

    @staticmethod
    def check_can_add(data: dict) -> bool:
        raise NotImplementedError

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # filter_by(...).update(...) is not working in inheritance
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        if hasattr(self, 'updated_on'):
            self.updated_on = db.func.now()
        db.session.commit()

    @validates('name')
    def validate_name(self, _, name):
        if '/' in name:
            raise ValueError('name cannot contain forward slash (/)')
        return name
