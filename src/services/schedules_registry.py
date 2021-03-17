import json
import logging
from typing import List, Dict

from gevent import thread

from src.event_dispatcher import EventDispatcher
from src.models.schedule.model_schedule import ScheduleModel
from src.services.event_service_base import Event, EventType
from src.services.mqtt_client import MqttRegistry
from src.utils import Singleton

logger = logging.getLogger(__name__)


class SchedulesRegistry(metaclass=Singleton):
    def __init__(self):
        self.__schedules: List[Dict[str, str]] = []

    @property
    def schedules(self) -> List[Dict[str, str]]:
        return self.__schedules

    def register(self):
        logger.info(f"Called schedules registration")
        schedules: List[ScheduleModel] = ScheduleModel.find_all()
        for schedule in schedules:
            self._add_schedule(schedule)
        while not all(mqtt_client.status() for mqtt_client in MqttRegistry().clients()):
            logger.warning('Waiting for MQTT connection to be connected...')
            thread.sleep(2)
        self._dispatch_event()
        logger.info(f"Finished schedules registration")

    @staticmethod
    def _create_schedule_registry(schedule: ScheduleModel):
        return {'uuid': schedule.uuid, 'name': schedule.name}

    def _add_schedule(self, schedule: ScheduleModel):
        self.__schedules.append(self._create_schedule_registry(schedule))

    def add_schedule(self, schedule: ScheduleModel):
        self._add_schedule(schedule)
        self._dispatch_event()

    def update_schedule(self, schedule: ScheduleModel):
        for idx, sch in enumerate(self.__schedules):
            if schedule.uuid == sch['uuid']:
                self.__schedules[idx] = self._create_schedule_registry(schedule)
                break
        self._dispatch_event()

    def delete_schedule(self, schedule: ScheduleModel):
        for idx, sch in enumerate(self.__schedules):
            if schedule.uuid == sch['uuid']:
                del self.__schedules[idx]
                break
        self._dispatch_event()

    def _dispatch_event(self):
        # TODO: better use of dispatching
        event = Event(EventType.SCHEDULES, json.dumps(self.__schedules))
        EventDispatcher().dispatch_from_service(None, event, None)
