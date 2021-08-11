from flask_restful import marshal_with

from src.models.schedule.model_schedule import ScheduleModel
from src.resources.rest_schema.schema_schedule import schedule_all_fields
from src.resources.schedule.schedule_base import ScheduleBase


class SchedulePlural(ScheduleBase):
    @classmethod
    @marshal_with(schedule_all_fields)
    def get(cls):
        schedules = ScheduleModel.find_all()
        return schedules

    @classmethod
    @marshal_with(schedule_all_fields)
    def post(cls):
        data = cls.parser.parse_args()
        return cls.add_schedule(data)
