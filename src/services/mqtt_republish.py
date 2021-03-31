import logging
from typing import List

from gevent import thread

from src.models.device.model_device import DeviceModel
from src.models.network.model_network import NetworkModel
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.mqtt_client import MqttRegistry
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttRepublish(metaclass=Singleton):
    def __init__(self):
        self.__points = None
        self.__networks = None
        self.__devices = None

    @property
    def points(self):
        return self.__points

    @property
    def networks(self):
        return self.__networks

    @property
    def devices(self):
        return self.__devices

    def republish(self):
        logger.info(f"Called mqtt republish")
        while not all(mqtt_client.status() for mqtt_client in MqttRegistry().clients()):
            logger.warning('Waiting for MQTT connection to be connected...')
            thread.sleep(2)
        self._publish_points()
        self._publish_networks()
        self._publish_devices()
        logger.info(f"Finished mqtt republish")

    def _publish_points(self):
        self.__points: List[PointModel] = PointModel.find_all()
        for point in self.__points:
            point.dispatch_event(point.to_dict())
            point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(point.uuid)
            point.publish_cov(point_store)

    def _publish_networks(self):
        self.__networks: List[NetworkModel] = NetworkModel.find_all()
        for network in self.__networks:
            network.dispatch_event(network.to_dict())

    def _publish_devices(self):
        self.__devices: List[DeviceModel] = DeviceModel.find_all()
        for device in self.__devices:
            device.dispatch_event(device.to_dict())
