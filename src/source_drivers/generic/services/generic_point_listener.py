from json import loads as json_loads, JSONDecodeError
from logging import Logger

from sqlalchemy.orm.exc import ObjectDeletedError

from src import db, GenericListenerSetting, MqttSetting
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase
from src.services.mqtt_client.mqtt_client_base import MqttClientBase
from src.source_drivers import GENERIC_SERVICE_NAME
from src.utils import Singleton


class MqttListenerMetadata(Singleton, type(MqttClientBase), type(EventServiceBase)):
    pass


class GenericPointListener(MqttClientBase, EventServiceBase, metaclass=MqttListenerMetadata):

    def __init__(self):
        MqttClientBase.__init__(self)
        EventServiceBase.__init__(self, GENERIC_SERVICE_NAME, False)

    @property
    def config(self) -> GenericListenerSetting:
        return self._config

    def start(self, config: MqttSetting, logger: Logger):
        super().start(config, logger)
        from src.event_dispatcher import EventDispatcher
        EventDispatcher().add_source_driver(self)

    def _on_connection_successful(self):
        self._logger.debug(f'MQTT sub to {self.config.topic}/#')
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
            self._logger.warning(f'Invalid generic point COV payload. point={point_name}, device={device_name}, '
                                 f'network={network_name}. error=({str(e)})')
            return

        point: PointModel = PointModel.find_by_name(point_name, device_name, network_name)
        if point is None or point.driver != GENERIC_SERVICE_NAME:
            self._logger.warning(f'Unknown generic point COV received with name={point_name}')
            return
        value = payload.get('value', None)
        value_raw = payload.get('value_raw', value)
        fault = payload.get('fault', None)
        fault_message = payload.get('fault_message', '')
        point_store = PointStoreModel(point_uuid=point.uuid, value_original=value, value_raw=value_raw, fault=fault,
                                      fault_message=fault_message)
        try:
            updated = point.update_point_value(point_store)
            if updated:
                point.publish_cov(point_store)
                db.session.commit()
        except ObjectDeletedError:
            self._logger.debug(f'Generic point removed when attempting to update point_store')
