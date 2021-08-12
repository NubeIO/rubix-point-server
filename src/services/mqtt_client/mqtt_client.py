import json
import logging
from typing import Callable, List, Union

from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info

from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.mqtt_client.mqtt_listener import MqttListener
from ...models.device.model_device import DeviceModel
from ...models.network.model_network import NetworkModel
from ...setting import MqttSetting

logger = logging.getLogger(__name__)

SERVICE_NAME_MQTT_CLIENT = 'mqtt'

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


class MqttClient(MqttListener):

    @property
    def config(self) -> MqttSetting:
        return super().config if isinstance(super().config, MqttSetting) else MqttSetting()

    @allow_only_on_prefix
    def start(self, config: MqttSetting, subscribe_topics: List[str] = None, callback: Callable = lambda: None):
        from .mqtt_registry import MqttRegistry
        MqttRegistry().add(self)
        super().start(config, subscribe_topics, callback)

    @classmethod
    def publish_point_cov(cls, driver_name, network: NetworkModel, device: DeviceModel, point: PointModel,
                          point_store: PointStoreModel, clear_value: bool, priority: int):
        payload: str = ''
        if not clear_value:
            output: dict = {
                'fault': point_store.fault,
                'value': point_store.value,
                'value_raw': point_store.value_raw,
                'ts': str(point_store.ts_value),
                'priority': priority
            }
            if point_store.fault:
                output = {**output, 'fault_message': point_store.fault_message, 'ts': str(point_store.ts_fault)}
            payload = json.dumps(output)

        from .mqtt_registry import MqttRegistry
        for client in MqttRegistry().clients():
            if client.config.publish_value:
                topic: str = client.__make_topic((client.config.topic, MQTT_TOPIC_COV, MQTT_TOPIC_COV_ALL,
                                                  driver_name,
                                                  network.uuid, network.name,
                                                  device.uuid, device.name,
                                                  point.uuid, point.name))
                client._publish_mqtt_value(topic, payload)

                if not point_store.fault:
                    topic: str = client.__make_topic((client.config.topic, MQTT_TOPIC_COV, MQTT_TOPIC_COV_VALUE,
                                                      driver_name,
                                                      network.uuid, network.name,
                                                      device.uuid, device.name,
                                                      point.uuid, point.name))
                    client._publish_mqtt_value(topic, '' if clear_value else str(point_store.value))

    @classmethod
    @allow_only_on_prefix
    def publish_debug(cls, payload: str):
        from .mqtt_registry import MqttRegistry
        for client in MqttRegistry().clients():
            if client.config.publish_debug:
                client._publish_mqtt_value(client.__make_topic((client.config.debug_topic,)), payload)

    @classmethod
    @allow_only_on_prefix
    def publish_point_registry(cls, payload: str):
        from .mqtt_registry import MqttRegistry
        for client in MqttRegistry().clients():
            if client.config.publish_value:
                client._publish_mqtt_value(client.__make_topic((client.config.topic, 'points')), payload)

    @classmethod
    @allow_only_on_prefix
    def publish_schedules(cls, payload: str):
        from .mqtt_registry import MqttRegistry
        for client in MqttRegistry().clients():
            if client.config.publish_value:
                client._publish_mqtt_value(client.__make_topic((client.config.topic, 'schedules')), payload)

    @classmethod
    @allow_only_on_prefix
    def publish_schedule_value(cls, topic: str, payload: str):
        from .mqtt_registry import MqttRegistry
        for client in MqttRegistry().clients():
            if client.config.publish_value:
                client._publish_mqtt_value(topic, payload)

    def _publish_mqtt_value(self, topic: str, payload: str, retain: bool = True):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        logger.debug(f"MQTT_PUBLISH: 'topic': {topic}, 'payload': {payload}, 'retain':{retain}")
        self.client.publish(topic, str(payload), qos=self.config.qos, retain=retain)

    @classmethod
    def prefix_topic(cls) -> str:
        device_info: Union[DeviceInfoModel, None] = get_device_info()
        if not device_info:
            logger.error('Please add device_info on Rubix Service')
            return ''
        return cls.SEPARATOR.join((device_info.client_id, device_info.client_name,
                                   device_info.site_id, device_info.site_name,
                                   device_info.device_id, device_info.device_name))

    @classmethod
    def __make_topic(cls, parts: tuple) -> str:
        return cls.SEPARATOR.join((cls.prefix_topic(),) + parts)
