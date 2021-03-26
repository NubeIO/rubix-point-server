import uuid as uuid_
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.schedule.model_schedule import ScheduleModel
from src.resources.rest_schema.schema_schedule import schedule_all_fields, schedule_all_attributes


class ScheduleResourceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in schedule_all_attributes:
        parser.add_argument(attr,
                            type=schedule_all_attributes[attr].get('type'),
                            required=schedule_all_attributes[attr].get('required', False),
                            help=schedule_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_schedule(cls, data):
        uuid = str(uuid_.uuid4())
        schedule = ScheduleModel(uuid=uuid, **data)
        schedule.save_to_db()
        return schedule


class ScheduleResource(ScheduleResourceBase):
    patch_parser = reqparse.RequestParser()
    for attr in schedule_all_attributes:
        patch_parser.add_argument(attr,
                                  type=schedule_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(schedule_all_fields)
    def get(cls, **kwargs):
        schedule: ScheduleModel = cls.get_schedule(**kwargs)
        if not schedule:
            raise NotFoundException('Schedule not found')
        return schedule

    @classmethod
    def delete(cls, **kwargs):
        schedule: ScheduleModel = cls.get_schedule(**kwargs)
        if not schedule:
            raise NotFoundException('Schedule not found')
        schedule.delete_from_db()
        return '', 204

    @classmethod
    @marshal_with(schedule_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        schedule: ScheduleModel = cls.get_schedule(**kwargs)
        if not schedule:
            return cls.add_schedule(data)
        return schedule.update(**data)

    @classmethod
    @marshal_with(schedule_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        schedule: ScheduleModel = cls.get_schedule(**kwargs)
        if not schedule:
            raise NotFoundException('Schedule not found')
        return schedule.update(**data)

    @classmethod
    @abstractmethod
    def get_schedule(cls, **kwargs) -> ScheduleModel:
        raise NotImplementedError


class ScheduleResourceByUUID(ScheduleResource):
    @classmethod
    def get_schedule(cls, **kwargs) -> ScheduleModel:
        return ScheduleModel.find_by_uuid(kwargs.get('uuid'))


class ScheduleResourceByName(ScheduleResource):
    @classmethod
    def get_schedule(cls, **kwargs) -> ScheduleModel:
        return ScheduleModel.find_by_name(kwargs.get('name'))


class ScheduleResourceList(ScheduleResourceBase):
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
