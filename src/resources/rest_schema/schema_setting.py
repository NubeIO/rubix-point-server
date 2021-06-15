from flask_restful import fields

from src.resources.utils import map_rest_schema

# Driver
driver_setting_all_attributes = {
    'uuid': {
        'type': str,
    },
    'generic': {
        'type': bool,
        'required': True,
    },
    'modbus_rtu': {
        'type': bool,
        'required': True,
    },
    'modbus_tcp': {
        'type': bool,
        'required': True,
    },
}

driver_setting_return_attributes = {
    'uuid': fields.String,
    'generic': fields.Boolean,
    'modbus_rtu': fields.Boolean,
    'modbus_tcp': fields.Boolean,
}

# Service
service_setting_all_attributes = {
    'uuid': {
        'type': str,
    },
    'mqtt': {
        'type': bool,
        'required': True,
    },
    'histories': {
        'type': bool,
        'required': True,
    },
    'cleaner': {
        'type': bool,
        'required': True,
    },
    'history_sync_influxdb': {
        'type': bool,
        'required': True,
    },
    'history_sync_postgres': {
        'type': bool,
        'required': True,
    },
}

service_setting_return_attributes = {
    'uuid': fields.String,
    'mqtt': fields.Boolean,
    'histories': fields.Boolean,
    'cleaner': fields.Boolean,
    'history_sync_influxdb': fields.Boolean,
    'history_sync_postgres': fields.Boolean,
}

# Influx
influx_setting_all_attributes = {
    'uuid': {
        'type': str,
    },
    'host': {
        'type': str,
        'required': True,
    },
    'port': {
        'type': int,
        'required': True,
    },
    'database': {
        'type': str,
        'required': True,
    },
    'username': {
        'type': str,
        'required': True,
    },
    'password': {
        'type': str,
        'required': True,
    },
    'ssl': {
        'type': bool,
        'required': True,
    },
    'verify_ssl': {
        'type': bool,
        'required': True,
    },
    'timeout': {
        'type': int,
        'required': True,
    },
    'retries': {
        'type': int,
        'required': True,
    },
    'timer': {
        'type': int,
        'required': True,
    },
    'path': {
        'type': str,
        'required': True,
    },
    'measurement': {
        'type': str,
        'required': True,
    },
    'attempt_reconnect_secs': {
        'type': int,
        'required': True,
    },
}

influx_setting_return_attributes = {
    'uuid': fields.String,
    'host': fields.String,
    'port': fields.Integer,
    'database': fields.String,
    'username': fields.String,
    'ssl': fields.Boolean,
    'verify_ssl': fields.Boolean,
    'timeout': fields.Integer,
    'retries': fields.Integer,
    'timer': fields.Integer,
    'path': fields.String,
    'measurement': fields.String,
    'attempt_reconnect_secs': fields.Integer,
}

# Postgres
postgres_setting_all_attributes = {
    'uuid': {
        'type': str,
    },
    'host': {
        'type': str,
        'required': True,
    },
    'port': {
        'type': int,
        'required': True,
    },
    'dbname': {
        'type': str,
        'required': True,
    },
    'user': {
        'type': str,
        'required': True,
    },
    'password': {
        'type': str,
        'required': True,
    },
    'ssl_mode': {
        'type': str,
        'required': True,
    },
    'connect_timeout': {
        'type': int,
        'required': True,
    },
    'timer': {
        'type': int,
        'required': True,
    },
    'table_prefix': {
        'type': str,
        'required': True,
    },
    'attempt_reconnect_secs': {
        'type': int,
        'required': True,
    }
}

postgres_setting_return_attributes = {
    'uuid': fields.String,
    'host': fields.String,
    'port': fields.Integer,
    'dbname': fields.String,
    'user': fields.String,
    'ssl_mode': fields.String,
    'connect_timeout': fields.Integer,
    'timer': fields.Integer,
    'table_prefix': fields.String,
    'attempt_reconnect_secs': fields.Integer
}

# Mqtt
mqtt_setting_all_attributes = {
    'uuid': {
        'type': str,
    },
    'enabled': {
        'type': bool,
        'required': True,
    },
    'name': {
        'type': str,
        'required': True,
    },
    'host': {
        'type': str,
        'required': True,
    },
    'port': {
        'type': int,
        'required': True,
    },
    'authentication': {
        'type': bool,
        'required': True,
    },
    'username': {
        'type': str,
        'required': True,
    },
    'password': {
        'type': str,
        'required': True,
    },
    'keepalive': {
        'type': int,
        'required': True,
    },
    'qos': {
        'type': int,
        'required': True,
    },
    'attempt_reconnect_on_unavailable': {
        'type': bool,
        'required': True,
    },
    'attempt_reconnect_secs': {
        'type': int,
        'required': True,
    },
    'timeout': {
        'type': int,
        'required': True,
    },
    'retain_clear_interval': {
        'type': int,
        'required': True,
    },
    'publish_value': {
        'type': bool,
        'required': True,
    },
    'topic': {
        'type': str,
        'required': True,
    },
    'listen': {
        'type': bool,
        'required': True,
    },
    'listen_topic': {
        'type': str,
        'required': True,
    },
    'publish_debug': {
        'type': bool,
        'required': True,
    },
    'debug_topic': {
        'type': str,
        'required': True,
    },
}

mqtt_setting_return_attributes = {
    'uuid': fields.String,
    'enabled': fields.Boolean,
    'name': fields.String,
    'host': fields.String,
    'port': fields.Integer,
    'authentication': fields.Boolean,
    'username': fields.String,
    'keepalive': fields.Integer,
    'qos': fields.Integer,
    'attempt_reconnect_on_unavailable': fields.Boolean,
    'attempt_reconnect_secs': fields.Integer,
    'timeout': fields.Integer,
    'retain_clear_interval': fields.Integer,
    'publish_value': fields.Boolean,
    'topic': fields.String,
    'listen': fields.Boolean,
    'listen_topic': fields.String,
    'publish_debug': fields.Boolean,
    'debug_topic': fields.String,
}
