from sqlalchemy import inspect
from sqlalchemy.orm import validates

from src import db
from src.utils import dbsession


class ModelBase(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        self.check_self()
        db.session.add(self)
        dbsession.commit(db)

    def save_to_db_no_commit(self):
        self.check_self()
        db.session.add(self)

    def delete_from_db(self):
        db.session.delete(self)
        dbsession.commit(db)

    @classmethod
    def create_temporary(cls, **kwargs):
        keys = kwargs.keys()
        for col in cls.__table__.c:
            if col.default is not None and col.description not in keys:
                kwargs[col.description] = col.default.arg
        return cls(**kwargs)

    # Issue #85 filter_by(...).update(...) is not working in inheritance
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        changed: bool = self.inspect_changes()
        self.check_self()
        dbsession.commit(db)
        return changed

    def check_self(self) -> (bool, any):
        return True

    def inspect_changes(self) -> bool:
        for attr in inspect(self).attrs:
            if attr.history.has_changes():
                return True
        return False

    @validates('name')
    def validate_name(self, _, name):
        if '/' in name:
            raise ValueError('name cannot contain forward slash (/)')
        return name

    def to_dict(self) -> dict:
        return {c.key: str(getattr(self, c.key))
                for c in inspect(self).mapper.column_attrs}
