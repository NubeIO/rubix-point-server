from sqlalchemy import inspect
from sqlalchemy.orm import validates

from src import db
from src.enums.model import ModelEvent
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import Event, EventType


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
        db.session.commit()
        self._dispatch_event(self._to_dict())

    def save_to_db_no_commit(self):
        self.check_self()
        db.session.add(self)
        self._dispatch_event(self._to_dict())

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        self._dispatch_event()

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
        db.session.commit()
        if changed:
            self._dispatch_event(kwargs)

    def get_model_event(self) -> ModelEvent:
        raise NotImplemented

    def get_model_event_type(self) -> EventType:
        raise NotImplemented

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

    def _to_dict(self) -> dict:
        return {c.key: str(getattr(self, c.key))
                for c in inspect(self).mapper.column_attrs}

    def _dispatch_event(self, payload: dict = {}):
        # TODO: better use of dispatching
        event = Event(self.get_model_event_type(), {
            'model': self,
            'payload': payload
        })
        EventDispatcher().dispatch_from_service(None, event, None)
