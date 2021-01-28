import logging
from json import loads as json_loads, JSONDecodeError

from src import GenericListenerSetting
from src.models.point.model_point import PointModel
from src.services.event_service_base import EventServiceBase
from src.services.mqtt_client.mqtt_client_base import MqttClientBase
from src.setting import MqttSettingBase
from src.source_drivers import GENERIC_SERVICE_NAME
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttListenerMetadata(Singleton, type(MqttClientBase), type(EventServiceBase)):
    pass


class GenericPointListener(MqttClientBase, EventServiceBase, metaclass=MqttListenerMetadata):

    def __init__(self):
        MqttClientBase.__init__(self)
        EventServiceBase.__init__(self, GENERIC_SERVICE_NAME, False)

    @property
    def config(self) -> GenericListenerSetting:
        return self._config

    def start(self, config: MqttSettingBase):
        from src.event_dispatcher import EventDispatcher
        EventDispatcher().add_source_driver(self)
        super().start(config)

    def _on_connection_successful(self):
        logger.debug(f'MQTT sub to {self.config.topic}/#')
        self._client.subscribe(f'{self.config.topic}/#')

    def _on_message(self, client, userdata, message):
        if self.config.topic in message.topic:
            self.__update_point(message)

    def _mqtt_topic_min(self):
        return len(self.make_topic((self.config.topic, '<point_name>', '<device_name>', '<network_name>')).split('/'))

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

        point: PointModel = PointModel.find_by_name(point_name, device_name, network_name)
        if point is None or point.driver != GENERIC_SERVICE_NAME:
            logger.warning(f'Unknown generic point COV received with point name={point_name}, device name={device_name}'
                           f', network name={network_name}')
            return
        value = payload.get('value', None)
        value_raw = payload.get('value_raw', value)
        fault = payload.get('fault', None)
        fault_message = payload.get('fault_message', '')
        try:
            point.update_point_store(value, value_raw, fault, fault_message)
        except Exception as e:
            logger.error(str(e))
