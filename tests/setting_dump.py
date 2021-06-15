from src import AppSetting

if __name__ == '__main__':
    setting = '''
    {
      "drivers": {
        "generic": false,
        "modbus_rtu": false,
        "modbus_tcp": false
      },
      "services": {
        "mqtt": true,
        "histories": true,
        "cleaner": true,
        "history_sync_influxdb": true,
        "history_sync_postgres": true
      },
      "influx": {
        "host": "0.0.0.0",
        "port": 8086,
        "database": "db",
        "username": "username",
        "password": "password",
        "ssl": false,
        "verify_ssl": false,
        "timeout": 5,
        "retries": 3,
        "timer": 5,
        "path": "",
        "measurement": "points",
        "attempt_reconnect_secs": 5
      },
      "postgres": {
        "host": "0.0.0.0",
        "port": 5432,
        "dbname": "db",
        "user": "user",
        "password": "password",
        "ssl_mode": "allow",
        "connect_timeout": 5,
        "timer": 5,
        "table_prefix": "tbl",
        "attempt_reconnect_secs": 5
      },
      "mqtt": [
        {
          "enabled": true,
          "name": "rubix-points",
          "host": "0.0.0.0",
          "port": 1883,
          "authentication": false,
          "username": "username",
          "password": "password",
          "keepalive": 60,
          "qos": 1,
          "attempt_reconnect_on_unavailable": true,
          "attempt_reconnect_secs": 5,
          "timeout": 10,
          "retain_clear_interval": 10,
          "publish_value": true,
          "topic": "rubix/points/value",
          "listen": true,
          "listen_topic": "rubix/points/listen",
          "publish_debug": true,
          "debug_topic": "rubix/points/debug"
        }
      ]
    }
    '''
    app_setting = AppSetting().reload(setting, is_json_str=True)
    print(type(app_setting.mqtt_settings))
    print(type(app_setting.services))
    print(type(app_setting.services.mqtt))
    print('-' * 30)
    assert len(app_setting.mqtt_settings) == 1
    print(app_setting.serialize())
    print('=' * 30)
    print('Default')
    print(AppSetting().serialize())
