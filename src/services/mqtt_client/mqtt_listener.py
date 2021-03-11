import json
import logging
from abc import abstractmethod
from typing import Callable, Union, List

from gevent import sleep
from paho.mqtt.client import MQTTMessage
from registry.registry import RubixRegistry
from rubix_mqtt.mqtt import MqttClientBase

from src import FlaskThread
from src.drivers.enums.drivers import Drivers
from src.enums.model import ModelEvent
from src.handlers.exception import exception_handler
from src.models.device.model_device import DeviceModel
from src.models.network.model_network import NetworkModel
from src.models.point.model_point import PointModel
from src.setting import MqttSetting

logger = logging.getLogger(__name__)


class MqttListener(MqttClientBase):
    SEPARATOR: str = '/'

    def __init__(self):
        self.__wires_plat: Union[dict, None] = None
        self.__config: Union[MqttSetting, None] = None
        MqttClientBase.__init__(self)

    @property
    def config(self) -> MqttSetting:
        return self.__config

    @property
    def wires_plat(self) -> Union[dict, None]:
        return self.__wires_plat

    def start(self, config: MqttSetting, subscribe_topics: List[str] = None, callback: Callable = lambda: None,
              loop_forever: bool = True):
        self.__config = config
        self.__wires_plat: dict = RubixRegistry().read_wires_plat()
        if not self.__wires_plat:
            logger.error('Please add wires-plat on Rubix Service')
            return
        subscribe_topics: List[str] = []
        if self.config.listen:
            # Resubscribe logic is not necessary here, these topics are for this app and will clear out when we start
            topic: str = self.__make_topic((self.get_listener_topic_prefix(), '#'))
            subscribe_topics.append(topic)
        if self.config.publish_value:
            topic: str = self.__make_topic((self.get_value_topic_prefix(), '#'))
            subscribe_topics.append(topic)
            FlaskThread(target=self.__resubscribe_value_topic, args=(topic,)).start()
        logger.info(f'Listening at: {subscribe_topics}')
        super().start(config, subscribe_topics, callback, loop_forever)

    def __resubscribe_value_topic(self, topic):
        """
        We resubscribe value topic for clearing un-necessary topic with retain on a certain interval of time
        For example: when we have points details on MQTT and we delete it, now it needs to be deleted from the MQTT
        broker too, this resubscribing logic does this on bulk.
        """
        while True:
            sleep(self.config.retain_clear_interval * 60)
            logger.info(f'Re-subscribing topic: {topic}')
            self.client.unsubscribe(topic)
            self.client.subscribe(topic)

    def get_listener_topic_prefix(self) -> str:
        return self.__make_topic((
            self.wires_plat.get('client_id'), self.wires_plat.get('site_id'), self.wires_plat.get('device_id'),
            self.config.listen_topic, 'cov'
        ))

    def get_value_topic_prefix(self) -> str:
        return self.__make_topic((
            self.wires_plat.get('client_id'), self.wires_plat.get('client_name'),
            self.wires_plat.get('site_id'), self.wires_plat.get('site_name'),
            self.wires_plat.get('device_id'), self.wires_plat.get('device_name'),
            self.config.topic
        ))

    @exception_handler
    def _on_message(self, client, userdata, message: MQTTMessage):
        if not message.payload:
            return
        if self.get_listener_topic_prefix() in message.topic:
            self.__update_generic_point(message)
        elif self.get_value_topic_prefix() in message.topic:
            self.__check_and_clear_value_topic(message)
        else:
            self.__clear_mqtt_retain_value(message)

    def __update_generic_point(self, message: MQTTMessage):
        topic: List[str] = message.topic.split(self.SEPARATOR)
        if len(topic) == self._mqtt_listener_topic_by_uuid_length() and topic[7] == 'uuid':
            self.__update_generic_point_by_uuid(topic, message)
        elif len(topic) == self._mqtt_listener_topic_by_name_length() and topic[7] == 'name':
            self.__update_generic_point_by_name(topic, message)
        self.__clear_mqtt_retain_value(message, force_clear=True)

    def __update_generic_point_by_uuid(self, topic: List[str], message: MQTTMessage):
        point_uuid: str = topic[-1]
        point: PointModel = PointModel.find_by_uuid(point_uuid)
        if point is None or (point and point.driver != Drivers.GENERIC):
            logger.warning(f'No point with point.uuid={point_uuid}')
        else:
            self.__update_generic_point_store(message, point)

    def __update_generic_point_by_name(self, topic: List[str], message: MQTTMessage):
        point_name: str = topic[-1]
        device_name: str = topic[-2]
        network_name: str = topic[-3]
        point: PointModel = PointModel.find_by_name(network_name, device_name, point_name)
        if point is None or (point and point.driver != Drivers.GENERIC):
            logger.warning(f'No point with network.name={network_name}, device.name={device_name}, '
                           f'point.name={point_name}')
        else:
            self.__update_generic_point_store(message, point)

    def __check_and_clear_value_topic(self, message: MQTTMessage):
        """
        Checks whether the subscribed data value exist or not on models, if it doesn't exist we clear retain value
        """
        topic: List[str] = message.topic.split(self.SEPARATOR)
        if len(topic) == self._mqtt_cov_value_topic():
            self.__check_and_clear_cov_point(topic, message)
        elif len(topic) == self._mqtt_update_value_topic():
            self.__check_and_clear_update_model(topic, message)
        elif not (len(topic) == self._mqtt_points_list_topic() and topic[-1] == 'points'):
            self.__clear_mqtt_retain_value(message)

    def __check_and_clear_cov_point(self, topic: List[str], message: MQTTMessage):
        point_name: str = topic[-1]
        point_uuid: str = topic[-2]
        device_name: str = topic[-3]
        device_uuid: str = topic[-4]
        network_name: str = topic[-5]
        network_uuid: str = topic[-6]
        if PointModel.find_by_uuid(point_uuid) is None or \
                PointModel.find_by_name(network_name, device_name, point_name) is None or \
                DeviceModel.find_by_uuid(device_uuid) is None or \
                NetworkModel.find_by_uuid(network_uuid) is None:
            logger.warning(f'No point with topic: {message.topic}')
            self.__clear_mqtt_retain_value(message)

    def __check_and_clear_update_model(self, topic: List[str], message: MQTTMessage):
        model_uuid: str = topic[-1]
        model_event: str = topic[-2]
        if model_event == ModelEvent.POINT.name:
            point: PointModel = PointModel.find_by_uuid(model_uuid)
            if point is None:
                logger.warning(f'No point with point.uuid={model_uuid}')
                self.__clear_mqtt_retain_value(message)
        elif model_event == ModelEvent.DEVICE.name:
            device: DeviceModel = DeviceModel.find_by_uuid(model_uuid)
            if device is None:
                logger.warning(f'No device with device.uuid={model_uuid}')
                self.__clear_mqtt_retain_value(message)
        elif model_event == ModelEvent.NETWORK.name:
            network: PointModel = DeviceModel.find_by_uuid(model_uuid)
            if network is None:
                logger.warning(f'No network with network.uuid={model_uuid}')
                self.__clear_mqtt_retain_value(message)
        else:
            self.__clear_mqtt_retain_value(message)

    def _mqtt_listener_topic_by_uuid_length(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<site_id>', '<device_id>', self.config.listen_topic, '<function>', 'uuid', '<point_uuid>'
        )).split(self.SEPARATOR))

    def _mqtt_listener_topic_by_name_length(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<site_id>', '<device_id>', self.config.listen_topic, '<function>', 'name',
            '<network_name>', '<device_name>', '<point_name>'
        )).split(self.SEPARATOR))

    def _mqtt_cov_value_topic(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<client_name>', '<site_id>', '<site_name>', '<device_id>', '<device_name>',
            self.config.topic, 'cov', '<type>', '<driver>', '<network_uuid>', '<network_name>',
            '<device_uuid>', '<device_name>', '<point_id>', '<point_name>'
        )).split(self.SEPARATOR))

    def _mqtt_update_value_topic(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<client_name>', '<site_id>', '<site_name>', '<device_id>', '<device_name>',
            self.config.topic, 'update', '<model>', '<model.uuid>'
        )).split(self.SEPARATOR))

    def _mqtt_points_list_topic(self) -> int:
        return len(self.__make_topic((
            '<client_id>', '<client_name>', '<site_id>', '<site_name>', '<device_id>', '<device_name>',
            self.config.topic, 'points'
        )).split(self.SEPARATOR))

    def __clear_mqtt_retain_value(self, message: MQTTMessage, force_clear: bool = False):
        """Clear retain value coz the point doesn't exist anymore"""
        if message.retain:
            logger.warning(f'Clearing topic: {message.topic}, having message: {message.payload}')
            self._publish_mqtt_value(message.topic, '', True)
        elif force_clear:
            logger.debug(f'Clearing topic: {message.topic}, having message: {message.payload}')
            self._publish_mqtt_value(message.topic, '', True)

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

    @abstractmethod
    def _publish_mqtt_value(self, topic: str, payload: str, retain: bool = False):
        raise NotImplementedError

    @classmethod
    def __make_topic(cls, parts: tuple) -> str:
        return cls.SEPARATOR.join(parts)
