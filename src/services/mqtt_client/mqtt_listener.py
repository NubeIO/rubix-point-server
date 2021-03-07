import logging
from json import loads as json_loads, JSONDecodeError
from typing import Callable

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
        subscribe_topic: str = self.__make_topic(
            (wires_plat.get('client_id'), wires_plat.get('site_id'), wires_plat.get('device_id'), config.listen_topic))
        logger.info(f'Listening at: {subscribe_topic}')
        super().start(config, subscribe_topic, callback, loop_forever)

    @exception_handler
    def _on_message(self, client, userdata, message):
        if self.config.listen_topic in message.topic:
            self.__update_point(message)

    def _mqtt_topic_min(self):
        return len(self.__make_topic(('<client_id>', '<site_id>', '<device_id>', self.config.topic, '<point_name>',
                                      '<device_name>', '<network_name>')).split('/'))

    def __update_point(self, message):
        topic = message.topic.split('/')
        if len(topic) != self._mqtt_topic_min():
            return
        point_name = topic[-3]
        device_name = topic[-2]
        network_name = topic[-1]
        try:
            payload = json_loads(message.payload)
            if not payload and ('value' not in payload.keys() or 'fault' not in payload.keys()):
                raise ValueError('No value or fault provided')
        except (JSONDecodeError, ValueError) as e:
            logger.warning(f'Invalid generic point COV payload. point={point_name}, device={device_name}, '
                           f'network={network_name}. error=({str(e)})')
            return

        point: PointModel = PointModel.find_by_name(network_name, device_name, point_name)
        if point is None or point.driver != Drivers.GENERIC:
            logger.warning(f'Unknown generic point COV received with point name={point_name}, device name={device_name}'
                           f', network name={network_name}')
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
        return MqttListener.SEPARATOR.join(parts)
