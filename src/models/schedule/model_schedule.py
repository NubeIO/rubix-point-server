import re

from sqlalchemy.orm import validates

from src import db
from src.enums.model import ModelEvent
from src.models.model_base import ModelBase
from src.services.event_service_base import EventType


class ScheduleModel(ModelBase):
    __tablename__ = 'schedules'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    def __repr__(self):
        return f"Schedule(uuid = {self.uuid})"

    def get_model_event(self) -> ModelEvent:
        return ModelEvent.SCHEDULE

    def get_model_event_type(self) -> EventType:
        return EventType.SCHEDULE_MODEL
