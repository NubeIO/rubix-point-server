import time
from abc import ABC, abstractmethod
from collections import Iterable
import logging

import paho.mqtt.client as mqtt

from src import MqttSetting


logger = logging.getLogger(__name__)


class MqttClientBase(ABC):

    def __init__(self):
        self._client = None
        self._config = None

    @property
    def config(self) -> MqttSetting:
        return self._config

    def start(self, config: MqttSetting):
        self._config = config
        logger.info(f'Starting MQTT client[{self.config.name}]...')
        self._client = mqtt.Client(self.config.name)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if self.config.attempt_reconnect_on_unavailable:
            while True:
                try:
                    self._client.connect(self.config.host, self.config.port, self.config.keepalive)
                    break
                except (ConnectionRefusedError, OSError) as e:
                    logger.error(
                        f'MQTT client[{self.config.name}] connection failure {self.to_string()} -> '
                        f'{type(e).__name__}. Attempting reconnect in '
                        f'{self.config.attempt_reconnect_secs} seconds')
                    time.sleep(self.config.attempt_reconnect_secs)
        else:
            try:
                self._client.connect(self.config.host, self.config.port, self.config.keepalive)
            except Exception as e:
                # catching so can set _client to None so publish_cov doesn't stack messages forever
                self._client = None
                logger.error(str(e))
                return
        logger.info(f'MQTT client {self.config.name} connected {self.to_string()}')
        self._client.loop_forever()

    def status(self) -> bool:
        return self.config and self.config.enabled and self._client and self._client.is_connected()

    def to_string(self) -> str:
        return f'{self.config.host}:{self.config.port}'

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - server unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            self._client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
        self._on_connection_successful()

    @abstractmethod
    def _on_connection_successful(self):
        pass

    @abstractmethod
    def _on_message(self, client, userdata, message):
        pass

    @abstractmethod
    def _mqtt_topic_min(self):
        pass

    @staticmethod
    def make_topic(part: Iterable, sep: str = '/'):
        return sep.join(part)
