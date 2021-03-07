import json
import logging
from typing import Callable

from registry.registry import RubixRegistry

from src.models.model_base import ModelBase
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, Event, EventType
from src.services.mqtt_client.mqtt_listener import MqttListener
from src.utils.model_utils import datetime_to_str
from .mqtt_registry import MqttRegistry
from ...setting import MqttSetting

logger = logging.getLogger(__name__)

SERVICE_NAME_MQTT_CLIENT = 'mqtt'

MQTT_TOPIC_ALL = 'all'
MQTT_TOPIC_DRIVER = 'driver'
MQTT_TOPIC_UPDATE = 'update'
MQTT_TOPIC_UPDATE_POINT = 'point'
MQTT_TOPIC_UPDATE_DEVICE = 'device'
MQTT_TOPIC_UPDATE_NETWORK = 'network'
MQTT_TOPIC_COV = 'cov'
MQTT_TOPIC_COV_ALL = 'all'
MQTT_TOPIC_COV_VALUE = 'value'


def allow_only_on_prefix(func):
    def inner_function(*args, **kwargs):
        prefix_topic: str = MqttClient.prefix_topic()
        if not prefix_topic:
            return
        func(*args, **kwargs)

    return inner_function


class MqttClient(MqttListener, EventServiceBase):

    def __init__(self):
        MqttListener.__init__(self)
        EventServiceBase.__init__(self, SERVICE_NAME_MQTT_CLIENT, False)
        self.supported_events[EventType.POINT_COV] = True
        self.supported_events[EventType.POINT_UPDATE] = True
        self.supported_events[EventType.DEVICE_UPDATE] = True
        self.supported_events[EventType.NETWORK_UPDATE] = True
        self.supported_events[EventType.MQTT_DEBUG] = True
        self.supported_events[EventType.POINT_REGISTRY_UPDATE] = True

    @property
    def config(self) -> MqttSetting:
        return super().config if isinstance(super().config, MqttSetting) else MqttSetting()

    def start(self, config: MqttSetting, subscribe_topic: str = None, callback: Callable = lambda: None,
              loop_forever: bool = True):
        from src.event_dispatcher import EventDispatcher
        EventDispatcher().add_service(self)
        MqttRegistry().add(self)
        super().start(config, subscribe_topic, callback, loop_forever)

    def _publish_cov(self, source_driver: str, network_uuid: str, network_name: str, device_uuid: str, device_name: str,
                     point: PointModel, point_store: PointStoreModel):
        if point is None or point_store is None or device_uuid is None or network_uuid is None or source_driver is \
                None or network_name is None or device_name is None:
            raise Exception('Invalid MQTT publish arguments')

        if point_store.fault:
            payload: dict = {
                'fault': point_store.fault,
                'fault_message': point_store.fault_message,
                'ts': point_store.ts_fault,
            }
        else:
            payload: dict = {
                'fault': point_store.fault,
                'value': point_store.value,
                'value_raw': point_store.value_raw,
                'ts': point_store.ts_value,
            }
        if not isinstance(payload['ts'], str):
            payload['ts'] = datetime_to_str(payload['ts'])

        topic: str = self.__make_topic((self.config.topic, MQTT_TOPIC_COV, MQTT_TOPIC_COV_ALL, source_driver,
                                        network_uuid, network_name,
                                        device_uuid, device_name,
                                        point.uuid, point.name))
        self._publish_mqtt_value(topic, json.dumps(payload))

        if self.config.publish_value and not point_store.fault:
            topic: str = self.__make_topic((self.config.topic, MQTT_TOPIC_COV, MQTT_TOPIC_COV_VALUE, source_driver,
                                            network_uuid, network_name,
                                            device_uuid, device_name,
                                            point.uuid, point.name))
            self._publish_mqtt_value(topic, str(point_store.value))

    def _publish_update(self, model: ModelBase, updates: dict):
        if model is None or updates is None or len(updates) == 0:
            raise Exception('Invalid MQTT publish arguments')
        topic: str = self.__make_topic(
            (self.config.topic, MQTT_TOPIC_UPDATE, model.get_model_event_name(), getattr(model, 'uuid', '<uuid>')))
        self._publish_mqtt_value(topic, json.dumps(updates))

    @allow_only_on_prefix
    def _run_event(self, event: Event):
        if event.data is None:
            return

        if event.event_type == EventType.MQTT_DEBUG:
            self._publish_mqtt_value(self.__make_topic((self.config.debug_topic,)), event.data)

        if event.event_type == EventType.POINT_REGISTRY_UPDATE:
            self._publish_mqtt_value(self.__make_topic((self.config.topic, 'points')), event.data)

        elif event.event_type == EventType.POINT_COV:
            self._publish_cov(event.data.get('source_driver'),
                              event.data.get('network').uuid, event.data.get('network').name,
                              event.data.get('device').uuid, event.data.get('device').name,
                              event.data.get('point'), event.data.get('point_store'))

        elif event.event_type == EventType.POINT_UPDATE or event.event_type == EventType.DEVICE_UPDATE or \
                event.event_type == EventType.NETWORK_UPDATE:
            self._publish_update(event.data.get('model'), event.data.get('updates'))

    def _publish_mqtt_value(self, topic: str, payload: str):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        logger.debug(f"MQTT_PUBLISH: 'topic': {topic}, 'payload': {payload}, 'retain': {self.config.retain}")
        self.client.publish(topic, str(payload), qos=self.config.qos, retain=self.config.retain)

    @classmethod
    def prefix_topic(cls) -> str:
        wires_plat: dict = RubixRegistry().read_wires_plat()
        if not wires_plat:
            logger.error('Please add wires-plat on Rubix Service')
            return ''
        return MqttClient.SEPARATOR.join((wires_plat.get('client_id'), wires_plat.get('client_name'),
                                          wires_plat.get('site_id'), wires_plat.get('site_name'),
                                          wires_plat.get('device_id'), wires_plat.get('device_name')))

    def __make_topic(self, parts: tuple) -> str:
        return MqttClient.SEPARATOR.join((self.prefix_topic(),) + parts)
