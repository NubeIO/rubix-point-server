import logging
from json import loads as json_loads, JSONDecodeError

from sqlalchemy.orm.exc import ObjectDeletedError

from src import db, EventDispatcher
from src.ini_config import *
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase
from src.services.mqtt_client.mqtt_client_base import MqttClientBase
from src.source_drivers.generic.services import GENERIC_SERVICE_NAME
from src.utils import Singleton

logger = logging.getLogger(__name__)

MQTT_CLIENT_NAME = 'rubix_points_generic_point'

GENERIC_POINT_MQTT_TOPIC = 'rubix/points/generic/cov'
GENERIC_POINT_MQTT_TOPIC_EXAMPLE = f'{GENERIC_POINT_MQTT_TOPIC}/<point_name>/<device_name>/<network_name>'
MQTT_TOPIC_MIN = len(GENERIC_POINT_MQTT_TOPIC_EXAMPLE.split('/'))


class GenericPointListener(MqttClientBase, EventServiceBase, metaclass=Singleton):
    service_name = GENERIC_SERVICE_NAME

    def __init__(self):
        MqttClientBase.__init__(
            self,
            generic_point__host,
            generic_point__port,
            generic_point__keepalive,
            generic_point__retain,
            generic_point__qos,
            generic_point__attempt_reconnect_on_unavailable,
            generic_point__attempt_reconnect_secs,
        )
        EventServiceBase.__init__(self)
        EventDispatcher().add_source_driver(self)

    def start(self, client_name: str = MQTT_CLIENT_NAME):
        logger.info(f"Generic Point MQTT listener started")
        MqttClientBase.start(self, client_name)

    def _on_connection_successful(self):
        logger.debug(f'MQTT sub to {GENERIC_POINT_MQTT_TOPIC}/#')
        self._client.subscribe(f'{GENERIC_POINT_MQTT_TOPIC}/#')

    def _on_message(self, client, userdata, message):
        if GENERIC_POINT_MQTT_TOPIC in message.topic:
            self.__update_point(message)

    def __update_point(self, message):
        topic = message.topic.split('/')
        if len(topic) != MQTT_TOPIC_MIN:
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
            logger.warning(f'Unknown generic point COV received with name={point_name}')
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
            logger.debug(f'Generic point removed when attempting to update point_store')
            return
