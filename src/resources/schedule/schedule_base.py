import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.models.schedule.model_schedule import ScheduleModel
from src.resources.rest_schema.schema_schedule import schedule_all_attributes


class ScheduleBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in schedule_all_attributes:
        parser.add_argument(attr,
                            type=schedule_all_attributes[attr].get('type'),
                            required=schedule_all_attributes[attr].get('required', False),
                            help=schedule_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_schedule(cls, data):
        uuid = str(shortuuid.uuid())
        schedule = ScheduleModel(uuid=uuid, **data)
        schedule.save_to_db()
        return schedule
