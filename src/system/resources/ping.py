import os
import time
from datetime import datetime

from flask_restful import Resource

from src.ini_config import config
from src.services.mqtt_client.mqtt_client import MqttClient

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
        enable_mqtt = config.getboolean('settings', 'enable_mqtt', fallback=False)
        enable_tcp = config.getboolean('settings', 'enable_tcp', fallback=False)
        enable_rtu = config.getboolean('settings', 'enable_rtu', fallback=False)
        enable_histories = config.getboolean('settings', 'enable_histories', fallback=False)
        enable_cleaner = config.getboolean('settings', 'enable_cleaner', fallback=False)
        return {
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            'deployment_mode': deployment_mode,
            'settings': {'enable_mqtt': enable_mqtt,
                         'enable_tcp': enable_tcp,
                         'enable_rtu': enable_rtu,
                         'enable_histories': enable_histories,
                         'enable_cleaner': enable_cleaner},
            'mqtt_status': MqttClient.get_instance().status()
        }
