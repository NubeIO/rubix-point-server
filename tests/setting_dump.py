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
        "history_sync": true,
        "history_sync_postgres": true
      },
      "influx": {
        "host": "0.0.0.0",
        "port": 8086,
        "database": "db",
        "username": "username",
        "password": "password",
        "verify_ssl": false,
        "timeout": 5,
        "retries": 3,
        "timer": 1,
        "path": "",
        "measurement": "history"
      },
      "generic_point_listener": {
        "enabled": true,
        "name": "rubix_points_generic_point",
        "host": "0.0.0.0",
        "port": 1883,
        "keepalive": 60,
        "qos": 1,
        "retain": false,
        "attempt_reconnect_on_unavailable": true,
        "attempt_reconnect_secs": 5,
        "publish_value": true,
        "topic": "rubix/points/generic/cov"
      },
      "mqtt": [
        {
          "enabled": true,
          "name": "rubix_points",
          "host": "0.0.0.0",
          "port": 1883,
          "keepalive": 60,
          "qos": 1,
          "retain": false,
          "attempt_reconnect_on_unavailable": true,
          "attempt_reconnect_secs": 5,
          "publish_value": true,
          "topic": "rubix/points"
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
