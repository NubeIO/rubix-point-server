import json
import logging
import time

import paho.mqtt.client as mqtt

from src.event_dispatcher import EventDispatcher
from src.ini_config import *
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


class MqttClient(EventServiceBase):
    service_name = SERVICE_NAME_MQTT_CLIENT
    threaded = False

    def __init__(self, host: str, port: int, keepalive: int, retain: bool, qos: int,
                 attempt_reconnect_on_unavailable: bool, attempt_reconnect_secs: int, publish_value: bool):
        super().__init__()
        self.__client = None
        self.__host = host
        self.__port = port
        self.__keepalive = keepalive
        self.__retain = retain
        self.__qos = qos
        self.__attempt_reconnect_on_unavailable = attempt_reconnect_on_unavailable
        self.__attempt_reconnect_secs = attempt_reconnect_secs
        self.__publish_value = publish_value
        self.supported_events[EventType.POINT_COV] = True
        self.supported_events[EventType.POINT_UPDATE] = True
        self.supported_events[EventType.DEVICE_UPDATE] = True
        self.supported_events[EventType.NETWORK_UPDATE] = True
        EventDispatcher.add_service(self)

    def to_string(self) -> str:
        return f'{self.__host}:{self.__port}'

    def status(self):
        if not self.__client:
            return False
        else:
            return self.__client.is_connected()

    def start(self):
        self.__client = mqtt.Client(MQTT_CLIENT_NAME)
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        if self.__attempt_reconnect_on_unavailable:
            while True:
                try:
                    self.__client.connect(self.__host, self.__port, self.__keepalive)
                    break
                except (ConnectionRefusedError, OSError) as e:
                    logger.error(
                        f'MQTT connection failure {self.__host}:{self.__port} -> '
                        f'{type(e).__name__}. Attempting reconnect in '
                        f'{self.__attempt_reconnect_secs} seconds')
                    time.sleep(self.__attempt_reconnect_secs)
        else:
            try:
                self.__client.connect(self.__host, self.__port, self.__keepalive)
            except Exception as e:
                # catching so can set __client to None so publish_cov doesn't stack messages forever
                self.__client = None
                logger.error(str(e))
                return
        logger.info(f'MQTT client connected {self.__host}:{self.__port}')
        self.__client.loop_forever()

    def publish_cov(self, point: PointModel, point_store: PointStoreModel, device_uuid: str, device_name: str,
                    network_uuid: str, network_name: str, source_driver: str):
        if not self.status():
            logger.error("MQTT is not connected...")
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

        logger.debug(f'MQTT PUB: {self.__host}:{self.__port} {topic} > {payload}')

        self.__client.publish(topic, json.dumps(payload), self.__qos, self.__retain)
        if self.__publish_value and not point_store.fault:
            topic.replace(MQTT_TOPIC_COV_ALL, MQTT_TOPIC_COV_VALUE, 1)
            logger.debug(f'MQTT PUB: {self.__host}:{self.__port} {topic} > {point_store.value}')
            self.__client.publish(topic, point_store.value, self.__qos, self.__retain)

    def publish_update(self, model: ModelBase, updates: dict):
        if not self.status():
            logger.error("MQTT is not connected...")
            return
        if model is None or updates is None or len(updates) == 0:
            raise Exception('Invalid MQTT publish arguments')

        topic = f'{MQTT_TOPIC}/{MQTT_TOPIC_UPDATE}/{model.get_model_event_name()}/{model.uuid}'

        logger.debug(f'MQTT PUB: {self.__host}:{self.__port} {topic} > {updates}')
        self.__client.publish(topic, json.dumps(updates), self.__qos, self.__retain)

    def __on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - server unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            self.__client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
        self.__client.subscribe(f'{MQTT_TOPIC}/#')

    def __on_message(self, client, userdata, message):
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


def create_mqtt_client(client_config_title: str) -> MqttClient:
    return MqttClient(
        config.get(client_config_title, 'host', fallback='0.0.0.0'),
        config.getint(client_config_title, 'port', fallback=1883),
        config.getint(client_config_title, 'keepalive', fallback=60),
        config.getboolean(client_config_title, 'retain', fallback=False),
        config.getint(client_config_title, 'qos', fallback=1),
        config.getboolean(client_config_title, 'attempt_reconnect_on_unavailable', fallback=True),
        config.getint(client_config_title, 'attempt_reconnect_secs', fallback=5),
        config.getboolean(client_config_title, 'publish_value', fallback=True),
    )
