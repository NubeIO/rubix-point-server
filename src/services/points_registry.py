import json
import logging
from typing import List, Dict

from gevent import thread

from src.drivers.enums.drivers import Drivers
from src.event_dispatcher import EventDispatcher
from src.models.point.model_point import PointModel
from src.services.event_service_base import Event, EventType
from src.services.mqtt_client import MqttRegistry
from src.utils import Singleton

logger = logging.getLogger(__name__)


class PointsRegistry(metaclass=Singleton):
    def __init__(self):
        self.__points: List[Dict[str, str]] = []

    @property
    def points(self) -> List[Dict[str, str]]:
        return self.__points

    def register(self):
        logger.info(f"Called points registration")
        points: List[PointModel] = PointModel.query.filter_by(driver=Drivers.GENERIC)
        for point in points:
            self._add_point(point)
        while not all(mqtt_client.status() for mqtt_client in MqttRegistry().clients()):
            logger.warning('Waiting for MQTT connection to be connected...')
            thread.sleep(2)
        self._dispatch_event()
        logger.info(f"Finished points registration")

    @staticmethod
    def _create_point_registry(point: PointModel):
        return {'uuid': point.uuid, 'name': f'{point.device.network.name}:{point.device.name}:{point.name}'}

    def _add_point(self, point: PointModel):
        self.__points.append(self._create_point_registry(point))

    def add_point(self, point: PointModel):
        self._add_point(point)
        self._dispatch_event()

    def update_point(self, point: PointModel):
        for idx, pnt in enumerate(self.__points):
            if point.uuid == pnt['uuid']:
                self.__points[idx] = self._create_point_registry(point)
                break
        self._dispatch_event()

    def delete_point(self, point: PointModel):
        for idx, pnt in enumerate(self.__points):
            if point.uuid == pnt['uuid']:
                del self.__points[idx]
                break
        self._dispatch_event()

    def _dispatch_event(self):
        # TODO: better use of dispatching
        event = Event(EventType.POINT_REGISTRY_UPDATE, json.dumps(self.__points))
        EventDispatcher().dispatch_from_service(None, event, None)
