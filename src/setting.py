import json
import os
from typing import List

from flask import Flask
from mrb.setting import MqttSetting as MqttRestBridgeSetting
from rubix_mqtt.setting import MqttSettingBase


class BaseSetting:

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting.get(k, v) for k, v in self.__dict__.items()}
        return self

    def serialize(self, pretty=True) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2 if pretty else None)

    def to_dict(self):
        return json.loads(self.serialize(pretty=False))


class ServiceSetting(BaseSetting):
    """
    Declares an availability service(enabled/disabled option)
    """

    KEY = 'services'

    def __init__(self):
        self.mqtt = True
        self.histories = False
        self.cleaner = False
        self.history_sync_influxdb = False
        self.history_sync_postgres = False


class DriverSetting(BaseSetting):
    """
    Declares an availability driver(enabled/disabled option)
    """

    KEY = 'drivers'

    def __init__(self):
        self.generic: bool = False
        self.modbus_rtu: bool = True
        self.modbus_tcp: bool = False
        self.bridge: bool = True


class MqttSetting(MqttSettingBase):
    KEY = 'mqtt'

    def __init__(self):
        super(MqttSetting, self).__init__()
        self.name = 'rubix-points'
        self.publish_value = True
        self.topic = 'rubix/points/value'
        self.publish_debug = True
        self.debug_topic = 'rubix/points/debug'


class GenericListenerSetting(MqttSettingBase):
    KEY = 'generic_point_listener'

    def __init__(self):
        super(GenericListenerSetting, self).__init__()
        self.name = 'rubix-points-generic-point-listener'
        self.topic = 'rubix/points/generic/cov'


class InfluxSetting(BaseSetting):
    KEY = 'influx'

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8086
        self.database = 'db'
        self.username = 'username'
        self.password = 'password'
        self.ssl = False
        self.verify_ssl = False
        self.timeout = 5
        self.retries = 3
        self.timer = 1
        self.path = ''
        self.measurement = 'history'
        self.attempt_reconnect_secs = 5


class PostgresSetting(BaseSetting):
    KEY = 'postgres'

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 5432
        self.dbname = 'db'
        self.user = 'user'
        self.password = 'password'
        self.ssl_mode = 'allow'
        self.connect_timeout = 5
        self.timer = 1
        self.table_name = 'point'
        self.attempt_reconnect_secs = 5


class CleanerSetting(BaseSetting):
    KEY = 'cleaner'

    def __init__(self):
        self.frequency = 5
        self.sleep = 10


class AppSetting:
    PORT: int = 1515
    GLOBAL_DIR_ENV = 'RUBIX_POINT_GLOBAL'
    DATA_DIR_ENV = 'RUBIX_POINT_DATA'
    CONFIG_DIR_ENV = 'RUBIX_POINT_CONFIG'
    KEY: str = 'APP_SETTING'
    default_global_dir = 'out'
    default_data_dir: str = 'data'
    default_config_dir: str = 'config'
    default_identifier: str = 'ps'
    default_setting_file: str = 'config.json'
    default_logging_conf: str = 'logging.conf'
    fallback_logging_conf: str = 'config/logging.example.conf'
    fallback_prod_logging_conf: str = 'config/logging.prod.example.conf'

    def __init__(self, **kwargs):
        self.__port = kwargs.get('port') or AppSetting.PORT
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), AppSetting.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('data_dir')),
                                             self.__join_global_dir(AppSetting.default_data_dir))
        self.__config_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('config_dir')),
                                               self.__join_global_dir(AppSetting.default_config_dir))
        self.__identifier = kwargs.get('identifier') or AppSetting.default_identifier
        self.__prod = kwargs.get('prod') or False
        self.__service_setting = ServiceSetting()
        self.__driver_setting = DriverSetting()
        self.__influx_setting = InfluxSetting()
        self.__postgres_setting = PostgresSetting()
        self.__listener_setting = GenericListenerSetting()
        self.__mqtt_rest_bridge_setting = MqttRestBridgeSetting()
        self.__mqtt_rest_bridge_setting.name = 'ps_mqtt_rest_bridge_listener'
        self.__mqtt_settings: List[MqttSetting] = [MqttSetting()]
        self.__cleaner_setting = CleanerSetting()

    @property
    def port(self):
        return self.__port

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def config_dir(self):
        return self.__config_dir

    @property
    def identifier(self):
        return self.__identifier

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def services(self) -> ServiceSetting:
        return self.__service_setting

    @property
    def drivers(self) -> DriverSetting:
        return self.__driver_setting

    @property
    def influx(self) -> InfluxSetting:
        return self.__influx_setting

    @property
    def postgres(self) -> PostgresSetting:
        return self.__postgres_setting

    @property
    def mqtt_settings(self) -> List[MqttSetting]:
        return self.__mqtt_settings

    @property
    def mqtt_rest_bridge_setting(self) -> MqttRestBridgeSetting:
        return self.__mqtt_rest_bridge_setting

    @property
    def listener(self) -> GenericListenerSetting:
        return self.__listener_setting

    @property
    def cleaner(self) -> CleanerSetting:
        return self.__cleaner_setting

    def serialize(self, pretty=True) -> str:
        m = {
            DriverSetting.KEY: self.drivers,
            ServiceSetting.KEY: self.services,
            InfluxSetting.KEY: self.influx,
            PostgresSetting.KEY: self.postgres,
            GenericListenerSetting.KEY: self.listener,
            MqttSetting.KEY: [s.to_dict() for s in self.mqtt_settings],
            CleanerSetting.KEY: self.cleaner,
            'prod': self.prod, 'global_dir': self.global_dir, 'data_dir': self.data_dir, 'config_dir': self.config_dir
        }
        return json.dumps(m, default=lambda o: o.to_dict() if isinstance(o, BaseSetting) else o.__dict__,
                          indent=2 if pretty else None)

    def reload(self, setting_file: str, is_json_str: bool = False):
        data = self.__read_file(setting_file, self.__config_dir, is_json_str)
        self.__driver_setting = self.__driver_setting.reload(data.get(DriverSetting.KEY))
        self.__service_setting = self.__service_setting.reload(data.get(ServiceSetting.KEY))
        self.__influx_setting = self.__influx_setting.reload(data.get(InfluxSetting.KEY))
        self.__postgres_setting = self.__postgres_setting.reload(data.get(PostgresSetting.KEY))
        self.__mqtt_rest_bridge_setting = self.__mqtt_rest_bridge_setting.reload(data.get('mqtt_rest_bridge_listener'))
        self.__listener_setting = self.__listener_setting.reload(data.get(GenericListenerSetting.KEY))
        self.__cleaner_setting = self.__cleaner_setting.reload(data.get(CleanerSetting.KEY))

        mqtt_settings = data.get(MqttSetting.KEY, [])
        if len(mqtt_settings) > 0:
            self.__mqtt_settings = [MqttSetting().reload(s) for s in mqtt_settings]
        return self

    def init_app(self, app: Flask):
        app.config[AppSetting.KEY] = self
        return self

    def __join_global_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__global_dir, _dir)

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __read_file(setting_file: str, _dir: str, is_json_str=False):
        if is_json_str:
            return json.loads(setting_file)
        if setting_file is None or setting_file.strip() == '':
            return {}
        s = setting_file if os.path.isabs(setting_file) else os.path.join(_dir, setting_file)
        if not os.path.isfile(s) or not os.path.exists(s):
            return {}
        with open(s) as json_file:
            return json.load(json_file)
