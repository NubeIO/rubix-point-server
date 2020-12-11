import time
from datetime import datetime

from flask_restful import Resource

from src.background import Background
from src.ini_config import *
from src.services.histories.sync.influxdb import InfluxDB

start_time = time.time()
up_time_date = str(datetime.now())


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
        deployment_mode = 'production' if os.environ.get("data_dir") is not None else 'development'
        mqtt_client_statuses = []
        for mqtt_client in Background.get_mqtt_client():
            mqtt_client_statuses.append({mqtt_client.to_string(): mqtt_client.status()})
        return {
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'mqtt_client_statuses': mqtt_client_statuses,
            'influx_db_status': InfluxDB.get_instance().status(),
            'settings': {
                'services': {
                    'mqtt': settings__enable_mqtt,
                    'histories': settings__enable_histories,
                    'cleaner': settings__enable_cleaner,
                    'history_sync': settings__enable_history_sync,
                },
                'drivers': {
                    'generic': settings__enable_generic,
                    'modbus_rtu': settings__enable_modbus_rtu,
                    'modbus_tcp': settings__enable_modbus_tcp,
                }
            }
        }
