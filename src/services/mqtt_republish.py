import logging
from typing import List

from gevent import thread

from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.mqtt_client import MqttRegistry
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttRepublish(metaclass=Singleton):
    @staticmethod
    def republish():
        logger.info(f"Called MQTT republish")
        while not all(mqtt_client.status() for mqtt_client in MqttRegistry().clients()):
            logger.warning('Waiting for MQTT connection to be connected...')
            thread.sleep(2)
        points: List[PointModel] = PointModel.find_all()
        for point in points:
            point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(point.uuid)
            if not point.disable_mqtt:
                point.publish_cov(point_store)
        logger.info(f"Finished MQTT republish")
