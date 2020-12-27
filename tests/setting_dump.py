import json
from configparser import ConfigParser
from io import StringIO

from src import ServiceSetting, DriverSetting, MqttSetting, InfluxSetting, GenericListenerSetting, AppSetting


def dump():
    _parser = ConfigParser()
    _parser[ServiceSetting.KEY] = ServiceSetting().__dict__
    _parser[DriverSetting.KEY] = DriverSetting().__dict__
    _parser[InfluxSetting.KEY] = InfluxSetting().__dict__
    _parser[GenericListenerSetting.KEY] = GenericListenerSetting().__dict__
    _parser['mqtt_local'] = MqttSetting().__dict__

    with StringIO() as ss:
        _parser.write(ss)
        ss.seek(0)
        return ss.read()


if __name__ == '__main__':
    setting = dump()
    print(setting)
    parser = ConfigParser()
    parser.read_string(setting)
    app_setting = AppSetting()._reload(parser)
    print(type(app_setting.services.mqtt))
    print(type(app_setting.influx.port))
    print(json.dumps(app_setting.services.__dict__))
