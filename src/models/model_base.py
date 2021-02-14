from sqlalchemy.orm import validates

from src import db
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

    def save_to_db_no_commit(self):
        self.check_self()
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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
        self.check_self()
        db.session.commit()
        event = Event(self.get_model_event_type(), {
            'model': self,
            'updates': kwargs
        })
        # TODO: source_driver name to publish change to source driver
        EventDispatcher().dispatch_from_service(None, event, None)

    def get_model_event_name(self) -> str:
        raise NotImplemented

    def get_model_event_type(self) -> EventType:
        raise NotImplemented

    def check_self(self) -> (bool, any):
        return True

    @validates('name')
    def validate_name(self, _, name):
        if '/' in name:
            raise ValueError('name cannot contain forward slash (/)')
        return name
