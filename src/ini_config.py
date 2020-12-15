"""Load configuration from .ini file."""
import configparser

import os

config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = 'settings/config.ini'
else:
    filename = os.path.join(os.environ.get("data_dir"), 'config.ini')

config.read(filename)

settings__enable_mqtt = config.getboolean('settings_services', 'enable_mqtt', fallback=False)
settings__enable_histories = config.getboolean('settings_services', 'enable_histories', fallback=False)
settings__enable_cleaner = config.getboolean('settings_services', 'enable_cleaner', fallback=False)
settings__enable_history_sync = config.getboolean('settings_services', 'enable_history_sync', fallback=False)

settings__enable_generic = config.getboolean('settings_drivers', 'enable_generic', fallback=False)
settings__enable_modbus_rtu = config.getboolean('settings_drivers', 'enable_modbus_rtu', fallback=False)
settings__enable_modbus_tcp = config.getboolean('settings_drivers', 'enable_modbus_tcp', fallback=False)

generic_point__host = config.get('generic_point_listener', 'host', fallback='0.0.0.0')
generic_point__port = config.getint('generic_point_listener', 'port', fallback=1883)
generic_point__keepalive = config.getint('generic_point_listener', 'keepalive', fallback=60)
generic_point__retain = config.getboolean('generic_point_listener', 'retain', fallback=False)
generic_point__qos = config.getint('generic_point_listener', 'qos', fallback=1)
generic_point__attempt_reconnect_on_unavailable = config.getboolean('generic_point_listener',
                                                                    'attempt_reconnect_on_unavailable', fallback=True)
generic_point__attempt_reconnect_secs = config.getint('generic_point_listener', 'attempt_reconnect_secs', fallback=5)

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
