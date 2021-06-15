import uuid as uuid_
import logging
from typing import List

from src import db
from src.models.setting.model_setting_base import SettingBaseModel
from src.setting import MqttSetting

logger = logging.getLogger(__name__)


class MqttSettingModel(SettingBaseModel):
    __tablename__ = 'setting_mqtt'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    enabled = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    host = db.Column(db.String(80), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    authentication = db.Column(db.Boolean(), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    keepalive = db.Column(db.Integer, nullable=False)
    qos = db.Column(db.Integer, nullable=False)
    attempt_reconnect_on_unavailable = db.Column(db.Boolean(), nullable=False)
    attempt_reconnect_secs = db.Column(db.Integer, nullable=False)
    timeout = db.Column(db.Integer, nullable=False)
    retain_clear_interval = db.Column(db.Integer, nullable=False)
    publish_value = db.Column(db.Boolean(), nullable=False)
    topic = db.Column(db.String(80), nullable=False)
    listen = db.Column(db.Boolean(), nullable=False)
    listen_topic = db.Column(db.String(80), nullable=False)
    publish_debug = db.Column(db.Boolean(), nullable=False)
    debug_topic = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"MqttSetting(uuid = {self.uuid})"

    @classmethod
    def create_default_if_does_not_exists(cls, configs: List[MqttSetting]):
        mqtt_settings = cls.find_all()
        if len(mqtt_settings) == 0:
            for config in configs:
                uuid = str(uuid_.uuid4())
                mqtt_setting = MqttSettingModel(uuid=uuid,
                                                enabled=config.enabled,
                                                name=config.name,
                                                host=config.host,
                                                port=config.port,
                                                authentication=config.authentication,
                                                username=config.username,
                                                password=config.password,
                                                keepalive=config.keepalive,
                                                qos=config.qos,
                                                attempt_reconnect_on_unavailable=
                                                config.attempt_reconnect_on_unavailable,
                                                attempt_reconnect_secs=config.attempt_reconnect_secs,
                                                timeout=config.timeout,
                                                retain_clear_interval=config.retain_clear_interval,
                                                publish_value=config.publish_value,
                                                topic=config.topic,
                                                listen=config.listen,
                                                listen_topic=config.listen_topic,
                                                publish_debug=config.publish_debug,
                                                debug_topic=config.debug_topic)

                mqtt_setting.save_to_db()
                mqtt_settings.append(mqtt_setting)
        return [MqttSetting().reload(s) for s in [ms.to_dict() for ms in mqtt_settings]]
