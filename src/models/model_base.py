from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

from src import db
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import Event, EventType


class ModelBase(db.Model):
    __abstract__ = True

    @declared_attr
    def created_on(cls):
        return db.Column(db.DateTime, server_default=db.func.now())

    @declared_attr
    def updated_on(cls):
        return db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def find_by_uuid(cls, device_uuid):
        return cls.query.filter_by(uuid=device_uuid).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        self.check_self()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Issue #85 filter_by(...).update(...) is not working in inheritance
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.check_self()
        db.session.commit()
        event = Event(self.get_model_event_type(), {
            'model': self,
            'updates': kwargs
        })
        # TODO: source_driver name to publish change to source driver
        EventDispatcher.dispatch_from_service(None, event, None)

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
