"""Load configuration from .ini file."""
import configparser

import os

config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = 'settings/config.ini'
else:
    filename = os.path.join(os.environ.get("data_dir"), 'config.ini')

config.read(filename)

settings__enable_mqtt = config.getboolean('settings', 'enable_mqtt', fallback=False)
settings__enable_tcp = config.getboolean('settings', 'enable_tcp', fallback=False)
settings__enable_rtu = config.getboolean('settings', 'enable_rtu', fallback=False)
settings__enable_histories = config.getboolean('settings', 'enable_histories', fallback=False)
settings__enable_cleaner = config.getboolean('settings', 'enable_cleaner', fallback=False)
settings__enable_history_sync = config.getboolean('settings', 'enable_history_sync', fallback=False)

mqtt__host = config.get('mqtt', 'host', fallback='0.0.0.0')
mqtt__port = config.getint('mqtt', 'port', fallback=1883)
mqtt__keepalive = config.getint('mqtt', 'keepalive', fallback=60)
mqtt__qos = config.getint('mqtt', 'qos', fallback=1)
mqtt__retain = config.getboolean('mqtt', 'retain', fallback=False)
mqtt__publish_value = config.getboolean('mqtt', 'publish_value', fallback=True)
mqtt__attempt_reconnect_on_unavailable = config.getboolean('mqtt', 'attempt_reconnect_on_unavailable', fallback=True)
mqtt__attempt_reconnect_secs = config.getint('mqtt', 'attempt_reconnect_secs', fallback=5)
mqtt__debug = config.getboolean('mqtt', 'debug', fallback=False)

influx_db__host = config.get('influx_db', 'host', fallback='0.0.0.0')
influx_db__port = config.getint('influx_db', 'port', fallback=8086)
influx_db__database = config.get('influx_db', 'database', fallback='db')
influx_db__username = config.get('influx_db', 'username', fallback='username')
influx_db__password = config.get('influx_db', 'password', fallback='password')
influx_db__verify_ssl = config.getboolean('influx_db', 'verify_ssl', fallback=False)
influx_db__timeout = config.getint('influx_db', 'timeout', fallback=5)
influx_db__retries = config.getint('influx_db', 'retries', fallback=3)
influx_db__timer = config.getint('influx_db', 'timer', fallback=1)
influx_db__path = config.get('influx_db', 'path', fallback=None)
influx_db__measurement = config.get('influx_db', 'measurement', fallback='history')
