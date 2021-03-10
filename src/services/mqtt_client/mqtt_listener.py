import json
import logging
from typing import Callable, Union

from paho.mqtt.client import MQTTMessage
from registry.registry import RubixRegistry
from rubix_mqtt.mqtt import MqttClientBase

from src.drivers.enums.drivers import Drivers
from src.handlers.exception import exception_handler
from src.models.point.model_point import PointModel
from src.setting import MqttSetting

logger = logging.getLogger(__name__)


class MqttListener(MqttClientBase):
    SEPARATOR: str = '/'

    def __init__(self):
        MqttClientBase.__init__(self)

    @property
    def config(self) -> MqttSetting:
        return super().config if isinstance(super().config, MqttSetting) else MqttSetting()

    def start(self, config: MqttSetting, subscribe_topic: str = None, callback: Callable = lambda: None,
              loop_forever: bool = True):
        wires_plat: dict = RubixRegistry().read_wires_plat()
        if not wires_plat:
            logger.error('Please add wires-plat on Rubix Service')
            return
        subscribe_topic: Union[str, None] = None
        if self.config.listen:
            subscribe_topic = self.__make_topic((
                wires_plat.get('client_id'), wires_plat.get('site_id'), wires_plat.get('device_id'),
                config.listen_topic, 'cov', '#'
            ))
            logger.info(f'Listening at: {subscribe_topic}')
        super().start(config, subscribe_topic, callback, loop_forever)

    @exception_handler
    def _on_message(self, client, userdata, message: MQTTMessage):
        if self.config.listen_topic in message.topic:
            self.__update_generic_point(message)

    def _mqtt_topic_by_uuid_length(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<site_id>', '<device_id>', self.config.listen_topic, '<function>', 'uuid', '<point_uuid>'
        )).split(self.SEPARATOR))

    def _mqtt_topic_by_name_length(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<site_id>', '<device_id>', self.config.listen_topic, '<function>', 'name',
            '<network_name>', '<device_name>', '<point_name>'
        )).split(self.SEPARATOR))

    def __update_generic_point(self, message: MQTTMessage):
        self.__update_generic_point_by_uuid(message)
        self.__update_generic_point_by_name(message)

    def __update_generic_point_by_uuid(self, message: MQTTMessage):
        topic = message.topic.split('/')
        if not (len(topic) == self._mqtt_topic_by_uuid_length() and topic[7] == 'uuid'):
            return
        point_uuid: str = topic[-1]
        point: PointModel = PointModel.find_by_uuid(point_uuid)
        if point is None or (point and point.driver != Drivers.GENERIC):
            logger.warning(f'No points with point.uuid={point_uuid}')
            return
        self.__update_generic_point_store(message, point)

    def __update_generic_point_by_name(self, message: MQTTMessage):
        topic = message.topic.split('/')
        if not (len(topic) == self._mqtt_topic_by_name_length() and topic[7] == 'name'):
            return
        point_name: str = topic[-1]
        device_name: str = topic[-2]
        network_name: str = topic[-3]
        point: PointModel = PointModel.find_by_name(network_name, device_name, point_name)
        if point is None or (point and point.driver != Drivers.GENERIC):
            logger.warning(f'No points with network.name={network_name}, device.name={device_name}, '
                           f'point.name={point_name}')
            return
        self.__update_generic_point_store(message, point)

    @staticmethod
    def __update_generic_point_store(message: MQTTMessage, point: PointModel):
        try:
            payload: dict = json.loads(message.payload)
        except Exception as e:
            logger.warning(f'Invalid generic point COV payload for point.uuid={point.uuid}. Here, error=({str(e)})')
            return
        value = payload.get('value', None)
        value_raw = payload.get('value_raw', None)
        fault = payload.get('fault', None)
        fault_message = payload.get('fault_message', '')
        priority = payload.get('priority', None)
        try:
            point.update_point_store(value, priority, value_raw, fault, fault_message)
        except Exception as e:
            logger.error(str(e))

    @classmethod
    def __make_topic(cls, parts: tuple):
        return cls.SEPARATOR.join(parts)
