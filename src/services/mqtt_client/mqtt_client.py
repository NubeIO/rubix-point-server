import json
import logging
import time

import paho.mqtt.client as mqtt

from src.event_dispatcher import EventDispatcher
from src.ini_config import config
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
    __instance = None
    __client = None
    __host = None
    __port = None
    __keepalive = None
    __qos = None
    __retain = None
    __publish_value = None
    __attempt_reconnect_on_unavailable = None
    __attempt_reconnect_secs = None
    __debug = None

    def __init__(self):
        if MqttClient.__instance:
            raise Exception("MqttClient class is a singleton class!")
        else:
            super().__init__()
            MqttClient.__host = config.get('mqtt', 'host', fallback='localhost')
            MqttClient.__port = config.getint('mqtt', 'port', fallback=1883)
            MqttClient.__keepalive = config.getint('mqtt', 'keepalive', fallback=60)
            MqttClient.__qos = config.getint('mqtt', 'qos', fallback=1)
            MqttClient.__retain = int(config.getboolean('mqtt', 'retain', fallback=True))
            MqttClient.__publish_value = config.getboolean('mqtt', 'publish_value', fallback=False)
            MqttClient.__attempt_reconnect_on_unavailable = config.getboolean('mqtt',
                                                                              'attempt_reconnect_on_unavailable',
                                                                              fallback=True)
            MqttClient.__attempt_reconnect_secs = config.getint('mqtt', 'attempt_reconnect_secs', fallback=5)
            MqttClient.__debug = config.getboolean('mqtt', 'debug', fallback=False)

            self.supported_events[EventType.POINT_COV] = True
            self.supported_events[EventType.POINT_UPDATE] = True
            self.supported_events[EventType.DEVICE_UPDATE] = True
            self.supported_events[EventType.NETWORK_UPDATE] = True
            EventDispatcher.add_service(self)
            MqttClient.__instance = self

    @staticmethod
    def get_instance():
        if MqttClient.__instance is None:
            MqttClient()
        return MqttClient.__instance

    @staticmethod
    def start():
        MqttClient.get_instance()
        MqttClient.__client = mqtt.Client(MQTT_CLIENT_NAME)
        MqttClient.__client.on_connect = MqttClient.__on_connect
        MqttClient.__client.on_message = MqttClient.__on_message
        if MqttClient.__attempt_reconnect_on_unavailable:
            while True:
                try:
                    MqttClient.__client.connect(MqttClient.__host, MqttClient.__port, MqttClient.__keepalive)
                    break
                except ConnectionRefusedError:
                    if MqttClient.__debug:
                        logger.info(
                            f'MQTT connection failure: ConnectionRefusedError. Attempting reconnect in '
                            f'{MqttClient.__attempt_reconnect_secs} seconds')
                    time.sleep(MqttClient.__attempt_reconnect_secs)
        else:
            try:
                MqttClient.__client.connect(MqttClient.__host, MqttClient.__port, MqttClient.__keepalive)
            except Exception as e:
                # catching so can set __client to None so publish_cov doesn't stack messages forever
                MqttClient.__client = None
                logger.error(str(e))
                return
        MqttClient.__client.loop_forever()

    @staticmethod
    def publish_cov(point: PointModel, point_store: PointStoreModel, device_uuid: str, device_name: str,
                    network_uuid: str, network_name: str, source_driver: str):
        if MqttClient.__client is None:
            return
        if point is None or point_store is None or device_uuid is None or network_uuid is None \
                or source_driver is None or network_name is None or device_name is None:
            raise Exception('Invalid MQTT publish arguments')

        topic = f'{MQTT_TOPIC}/{MQTT_TOPIC_COV}/{MQTT_TOPIC_COV_ALL}/{point.uuid}/{point.name}/' \
                f'{device_uuid}/{device_name}/{network_uuid}/{network_name}/{source_driver}'

        payload = {
            'value': point_store.value,
            'value_array': point_store.value_array,
            'fault': point_store.fault,
            'fault_message': point_store.fault_message,
        }
        if MqttClient.__debug:
            logger.info(f'MQTT PUB: {topic} > {payload}')
        MqttClient.__client.publish(topic, json.dumps(payload), MqttClient.__qos, MqttClient.__retain)
        if MqttClient.__publish_value and not point_store.fault:
            topic.replace(MQTT_TOPIC_COV_ALL, MQTT_TOPIC_COV_VALUE, 1)
            if MqttClient.__debug:
                logger.info(f'MQTT PUB: {topic} > {point_store.value}')
            MqttClient.__client.publish(topic, point_store.value, MqttClient.__qos, MqttClient.__retain)

    @staticmethod
    def publish_update(model: ModelBase, updates: dict):
        if MqttClient.__client is None:
            return
        if model is None or updates is None or len(updates) == 0:
            raise Exception('Invalid MQTT publish arguments')

        topic = f'{MQTT_TOPIC}/{MQTT_TOPIC_UPDATE}/{model.get_model_event_name()}/{model.uuid}'

        if MqttClient.__debug:
            logger.info(f'MQTT PUB: {topic} > {updates}')
        MqttClient.__client.publish(topic, json.dumps(updates), MqttClient.__qos, MqttClient.__retain)

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - server unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            MqttClient.__client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
        MqttClient.__client.subscribe(f'{MQTT_TOPIC}/#')

    @staticmethod
    def __on_message(client, userdata, message):
        pass
        # topic_split = message.topic.split('/')
        # if len(topic_split) < MQTT_TOPIC_MIN:
        #     return
        # if topic_split[MQTT_TOPIC_MIN] == MQTT_TOPIC_ALL:
        #     MqttClient.__handle_all_message(topic_split, message)
        # elif topic_split[MQTT_TOPIC_MIN] == MQTT_TOPIC_DRIVER:
        #     MqttClient.__handle_driver_message(topic_split, message)
        # else:
        #     return

    @staticmethod
    def __handle_all_message(topic_split, message):
        pass

    @staticmethod
    def __handle_driver_message(topic_split, message):
        pass

    def _run_event(self, event: Event):
        if event.data is None:
            return

        if event.event_type == EventType.POINT_COV:
            MqttClient.publish_cov(event.data.get('point'), event.data.get('point_store'),
                                   event.data.get('device').uuid, event.data.get('device').name,
                                   event.data.get('network').uuid, event.data.get('network').name,
                                   event.data.get('source_driver'))

        elif event.event_type == EventType.POINT_UPDATE or EventType.DEVICE_UPDATE or EventType.NETWORK_UPDATE:
            MqttClient.publish_update(event.data.get('model'), event.data.get('updates'))
