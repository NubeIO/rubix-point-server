import time
from datetime import datetime

from flask import current_app
from rubix_http.resource import RubixResource

from src.utils.project import get_version

start_time = time.time()
up_time_date = str(datetime.now())


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - start_time


class Ping(RubixResource):

    @classmethod
    def get(cls):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        from src import AppSetting
        from src.services.histories.sync.influxdb import InfluxDB
        from src.services.histories.sync.postgresql import PostgreSQL
        from src.services.mqtt_client import MqttRegistry
        setting: AppSetting = current_app.config[AppSetting.KEY]
        deployment_mode = 'production' if setting.prod else 'development'
        return {
            'version': get_version(),
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'mqtt_client_statuses': [{mqttc.to_string(): mqttc.status()} for mqttc in MqttRegistry().clients()],
            'influx_db_status': InfluxDB().status(),
            'postgre_sql_status': PostgreSQL().status(),
            'settings': {
                setting.services.KEY: setting.services.to_dict(),
                setting.drivers.KEY: setting.drivers.to_dict()
            }
        }
