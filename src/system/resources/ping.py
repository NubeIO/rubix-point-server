import time
from datetime import datetime

from flask import current_app
from flask_restful import Resource

start_time = time.time()
up_time_date = str(datetime.now())
with open('VERSION') as version_file:
    version = version_file.read().strip()


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - start_time


class Ping(Resource):

    def get(self):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = "{:.2f}".format(up_min)
        up_hour = up_time / 3600
        up_hour = "{:.2f}".format(up_hour)
        from src import AppSetting
        from src.services.histories.sync.influxdb import InfluxDB
        from src.services.mqtt_client import MqttRegistry
        setting: AppSetting = current_app.config[AppSetting.KEY]
        deployment_mode = 'production' if setting.prod else 'development'
        return {
            'version': version,
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'mqtt_client_statuses': [{mqttc.to_string(): mqttc.status()} for mqttc in MqttRegistry().clients()],
            'influx_db_status': InfluxDB().status(),
            'settings': {
                'services': {
                    'mqtt': setting.services.mqtt,
                    'histories': setting.services.histories,
                    'cleaner': setting.services.cleaner,
                    'history_sync': setting.services.history_sync,
                },
                'drivers': {
                    'generic': setting.drivers.generic,
                    'modbus_rtu': setting.drivers.modbus_rtu,
                    'modbus_tcp': setting.drivers.modbus_tcp,
                }
            }
        }
