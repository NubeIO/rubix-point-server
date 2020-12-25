import json
import logging

from src.services.mqtt_client.mqtt_client_base import MqttClientBase
from src.event_dispatcher import EventDispatcher
from src.models.model_base import ModelBase
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, Event, EventType

SERVICE_NAME_MQTT_CLIENT = 'mqtt'

MQTT_CLIENT_NAME = 'rubix_points'
MQTT_TOPIC = 'rubix/points'
MQTT_TOPIC_MIN = len(MQTT_TOPIC.split('/')) + 1
MQTT_TOPIC_ALL = 'all'
MQTT_TOPIC_DRIVER = 'driver'
MQTT_TOPIC_UPDATE = 'update'
MQTT_TOPIC_UPDATE_POINT = 'point'
MQTT_TOPIC_UPDATE_DEVICE = 'device'
MQTT_TOPIC_UPDATE_NETWORK = 'network'
MQTT_TOPIC_COV = 'cov'
MQTT_TOPIC_COV_ALL = 'all'
MQTT_TOPIC_COV_VALUE = 'value'

logger = logging.getLogger(__name__)


class MqttClient(MqttClientBase, EventServiceBase):
    service_name = SERVICE_NAME_MQTT_CLIENT
    threaded = False

    def __init__(self, host: str, port: int, keepalive: int, retain: bool, qos: int,
                 attempt_reconnect_on_unavailable: bool, attempt_reconnect_secs: int, publish_value: bool):
        MqttClientBase.__init__(self, host, port, keepalive, retain, qos, attempt_reconnect_on_unavailable,
                                attempt_reconnect_secs)
        EventServiceBase.__init__(self)

        self.__publish_value = publish_value

        self.supported_events[EventType.POINT_COV] = True
        self.supported_events[EventType.POINT_UPDATE] = True
        self.supported_events[EventType.DEVICE_UPDATE] = True
        self.supported_events[EventType.NETWORK_UPDATE] = True
        EventDispatcher().add_service(self)

    def start(self, client_name: str = MQTT_CLIENT_NAME):
        logger.info(f"MQTT Client {self.to_string()} started")
        MqttClientBase.start(self, client_name)

    def publish_cov(self, point: PointModel, point_store: PointStoreModel, device_uuid: str, device_name: str,
                    network_uuid: str, network_name: str, source_driver: str):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        if point is None or point_store is None or device_uuid is None or network_uuid is None \
                or source_driver is None or network_name is None or device_name is None:
            raise Exception('Invalid MQTT publish arguments')

        topic = f'{MQTT_TOPIC}/{MQTT_TOPIC_COV}/{MQTT_TOPIC_COV_ALL}/{point.uuid}/{point.name}/' \
                f'{device_uuid}/{device_name}/{network_uuid}/{network_name}/{source_driver}'

        payload = {
            'value': point_store.value,
            'value_raw': point_store.value_raw,
            'fault': point_store.fault,
            'fault_message': point_store.fault_message,
        }

        logger.debug(f'MQTT PUB: {self.to_string()} {topic} > {payload}')

        self._client.publish(topic, json.dumps(payload), self._qos, self._retain)
        if self.__publish_value and not point_store.fault:
            topic.replace(MQTT_TOPIC_COV_ALL, MQTT_TOPIC_COV_VALUE, 1)
            logger.debug(f'MQTT PUB: {self.to_string()} {topic} > {point_store.value}')
            self._client.publish(topic, point_store.value, self._qos, self._retain)

    def publish_update(self, model: ModelBase, updates: dict):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        if model is None or updates is None or len(updates) == 0:
            raise Exception('Invalid MQTT publish arguments')

        topic = f'{MQTT_TOPIC}/{MQTT_TOPIC_UPDATE}/{model.get_model_event_name()}/{model.uuid}'

        logger.debug(f'MQTT PUB: {self.to_string()} {topic} > {updates}')
        self._client.publish(topic, json.dumps(updates), self._qos, self._retain)

    def _on_connection_successful(self):
        self._client.subscribe(f'{MQTT_TOPIC}/#')

    def _on_message(self, client, userdata, message):
        pass
        # topic_split = message.topic.split('/')
        # if len(topic_split) < MQTT_TOPIC_MIN:
        #     return
        # if topic_split[MQTT_TOPIC_MIN] == MQTT_TOPIC_ALL:
        #     self.__handle_all_message(topic_split, message)
        # elif topic_split[MQTT_TOPIC_MIN] == MQTT_TOPIC_DRIVER:
        #     self.__handle_driver_message(topic_split, message)
        # else:
        #     return

    def __handle_all_message(self, topic_split, message):
        pass

    def __handle_driver_message(self, topic_split, message):
        pass

    def _run_event(self, event: Event):
        if event.data is None:
            return

        if event.event_type == EventType.POINT_COV:
            self.publish_cov(event.data.get('point'), event.data.get('point_store'),
                             event.data.get('device').uuid, event.data.get('device').name,
                             event.data.get('network').uuid, event.data.get('network').name,
                             event.data.get('source_driver'))

        elif event.event_type == EventType.POINT_UPDATE or event.event_type == EventType.DEVICE_UPDATE or \
                event.event_type == EventType.NETWORK_UPDATE:
            self.publish_update(event.data.get('model'), event.data.get('updates'))
