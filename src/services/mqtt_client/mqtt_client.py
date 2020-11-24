import paho.mqtt.client as mqtt
import json
import time

# from src.ini_config import config
from src.services.event_service_base import EventServiceBase, Event, EventTypes
from src.event_dispatcher import EventDispatcher
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel

SERVICE_NAME_MQTT_CLIENT = 'mqtt'

MQTT_CLIENT_NAME = 'rubix_points'
MQTT_TOPIC = 'rubix/points'
MQTT_TOPIC_MIN = len(MQTT_TOPIC.split('/')) + 1
MQTT_TOPIC_ALL = 'all'
MQTT_TOPIC_DRIVER = 'driver'

DEFAULT_host = 'localhost'
DEFAULT_port = 1883
DEFAULT_keepalive = 60
DEFAULT_qos = 1
DEFAULT_retain = True
DEFAULT_publish_value = False
DEFAULT_attempt_reconnect_on_unavailable = True
DEFAULT_attempt_reconnect_secs = 5
DEFAULT_debug = False


class MqttClient(EventServiceBase):
    service_name = SERVICE_NAME_MQTT_CLIENT
    threaded = False
    __instance = None
    __client = None
    __keepalive = DEFAULT_keepalive
    __qos = DEFAULT_qos
    __retain = DEFAULT_retain
    __publish_value = DEFAULT_publish_value
    __attempt_reconnect_on_unavailable = DEFAULT_attempt_reconnect_on_unavailable
    __attempt_reconnect_secs = DEFAULT_attempt_reconnect_secs
    __debug = DEFAULT_debug

    def __init__(self):
        if MqttClient.__instance:
            raise Exception("MqttClient class is a singleton class!")
        else:
            super().__init__()
            # MqttClient.__keepalive = config.getint('mqtt', 'keepalive', fallback=DEFAULT_keepalive)
            # MqttClient.__qos = config.getint('mqtt', 'qos', fallback=DEFAULT_qos)
            # MqttClient.__retain = int(config.getboolean('mqtt', 'retain', fallback=DEFAULT_retain))
            # MqttClient.__publish_value = config.getboolean('mqtt', 'publish_value', fallback=DEFAULT_publish_value)
            # MqttClient.__attempt_reconnect_on_unavailable = config.getboolean(
            #     'mqtt', 'attempt_reconnect_on_unavailable', fallback=DEFAULT_attempt_reconnect_on_unavailable)
            # MqttClient.__attempt_reconnect_secs = config.getint('mqtt', 'attempt_reconnect_secs',
            #                                             fallback=DEFAULT_attempt_reconnect_secs)
            # MqttClient.__debug = config.getboolean('mqtt', 'debug', fallback=DEFAULT_debug)
            self.supported_events[EventTypes.POINT_COV] = True
            EventDispatcher.add_service(self)
            MqttClient.__instance = self

    @staticmethod
    def get_instance():
        if MqttClient.__instance is None:
            MqttClient()
        return MqttClient.__instance

    @staticmethod
    def start():
        # TODO: remove when .ini added
        raise Exception('.ini config not implemented')
        # try:
        # host = config.get('mqtt', 'host', fallback=DEFAULT_host)
        # port = config.getint('mqtt', 'port', fallback=DEFAULT_port)
        #
        # MqttClient.start(host, MqttClient.__port, MqttClient.__keepalive, MqttClient.__qos, MqttClient.__retain)
        # except Exception as e:
        #     print('MQTT Error', e)

    @staticmethod
    def start(host: str, port: int = DEFAULT_port, keepalive: int = DEFAULT_keepalive,
              qos: int = DEFAULT_qos, retain: bool = DEFAULT_retain):
        MqttClient.get_instance()
        MqttClient.__client = mqtt.Client(MQTT_CLIENT_NAME)
        MqttClient.__qos = qos
        MqttClient.__retain = retain
        MqttClient.__client.on_connect = MqttClient.__on_connect
        MqttClient.__client.on_message = MqttClient.__on_message
        if MqttClient.__attempt_reconnect_on_unavailable:
            while True:
                try:
                    MqttClient.__client.connect(host, port, keepalive)
                    break
                except ConnectionRefusedError:
                    if MqttClient.__debug:
                        print('MQTT connection failure: ConnectionRefusedError. Attempting reconnect in',
                              MqttClient.__attempt_reconnect_secs, 'seconds')
                    time.sleep(MqttClient.__attempt_reconnect_secs)
        else:
            try:
                MqttClient.__client.connect(host, port, keepalive)
            except Exception as e:
                # catching so can set __client to None so publish_cov doesn't stack messages forever
                MqttClient.__client = None
                raise e
        MqttClient.__client.loop_forever()

    @staticmethod
    def publish_cov(point: PointModel, point_store: PointStoreModel, device_uuid: str, device_name: str,
                    network_uuid: str, network_name: str, source_driver: str):
        if MqttClient.__client is None:
            return
        if point is None or point_store is None or device_uuid is None or network_uuid is None \
                or source_driver is None or network_name is None or device_name is None:
            raise Exception('Bad MQTT publish arguments')
        topic = f'{MQTT_TOPIC}/{source_driver}/{network_uuid}/{network_name}/{device_uuid}/{device_name}' \
                f'/{point.uuid}/{point.name}'

        payload = {
            'value': point_store.value,
            'value_array': point_store.value_array,
            'fault': point_store.fault,
            'fault_message': point_store.fault_message,
        }
        if MqttClient.__debug:
            print('MQTT PUB:', topic + '/data', payload)
        MqttClient.__client.publish(topic + '/data', json.dumps(payload), MqttClient.__qos, MqttClient.__retain)
        if MqttClient.__publish_value and not point_store.fault:
            if MqttClient.__debug:
                print('MQTT PUB', topic + '/value', point_store.value)
            MqttClient.__client.publish(topic + '/value', point_store.value, MqttClient.__qos, MqttClient.__retain)

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
        #     MqttClient.__handleAllMessage(topic_split, message)
        # elif topic_split[MQTT_TOPIC_MIN] == MQTT_TOPIC_DRIVER:
        #     MqttClient.__handleDriverMessage(topic_split, message)
        # else:
        #     return

    @staticmethod
    def __handleAllMessage(topic_split, message):
        pass

    @staticmethod
    def __handleDriverMessage(topic_split, message):
        pass

    def _run_event(self, event: Event):
        if event.event_type == EventTypes.POINT_COV:
            if event.data is not None:
                # TODO: maybe data checking or leave up to developer to speed up?
                MqttClient.publish_cov(event.data.get('point'), event.data.get('point_store'),
                                       event.data.get('device').uuid, event.data.get('device').name,
                                       event.data.get('network').uuid, event.data.get('network').name,
                                       event.data.get('source_driver'))
