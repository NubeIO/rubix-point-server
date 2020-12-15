import logging
import time

import paho.mqtt.client as mqtt

from src.ini_config import *

logger = logging.getLogger(__name__)


class MqttClientBase:

    def __init__(self, host: str, port: int, keepalive: int, retain: bool, qos: int,
                 attempt_reconnect_on_unavailable: bool, attempt_reconnect_secs: int):
        self._client = None
        self._host = host
        self._port = port
        self._keepalive = keepalive
        self._retain = retain
        self._qos = qos
        self._attempt_reconnect_on_unavailable = attempt_reconnect_on_unavailable
        self._attempt_reconnect_secs = attempt_reconnect_secs

    def to_string(self) -> str:
        return f'{self._host}:{self._port}'

    def status(self):
        if not self._client:
            return False
        else:
            return self._client.is_connected()

    def start(self, client_name: str):
        self._client = mqtt.Client(client_name)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if self._attempt_reconnect_on_unavailable:
            while True:
                try:
                    self._client.connect(self._host, self._port, self._keepalive)
                    break
                except (ConnectionRefusedError, OSError) as e:
                    logger.error(
                        f'MQTT client {client_name} connection failure {self.to_string()} -> '
                        f'{type(e).__name__}. Attempting reconnect in '
                        f'{self._attempt_reconnect_secs} seconds')
                    time.sleep(self._attempt_reconnect_secs)
        else:
            try:
                self._client.connect(self._host, self._port, self._keepalive)
            except Exception as e:
                # catching so can set _client to None so publish_cov doesn't stack messages forever
                self._client = None
                logger.error(str(e))
                return
        logger.info(f'MQTT client {client_name} connected {self.to_string()}')
        self._client.loop_forever()

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

    def _on_connection_successful(self):
        return

    def _on_message(self, client, userdata, message):
        return


def create_mqtt_client(client_config_title: str, mqtt_class: MqttClientBase.__class__) -> MqttClientBase:
    return mqtt_class(
        config.get(client_config_title, 'host', fallback='0.0.0.0'),
        config.getint(client_config_title, 'port', fallback=1883),
        config.getint(client_config_title, 'keepalive', fallback=60),
        config.getboolean(client_config_title, 'retain', fallback=False),
        config.getint(client_config_title, 'qos', fallback=1),
        config.getboolean(client_config_title, 'attempt_reconnect_on_unavailable', fallback=True),
        config.getint(client_config_title, 'attempt_reconnect_secs', fallback=5),
        config.getboolean(client_config_title, 'publish_value', fallback=True),
    )
