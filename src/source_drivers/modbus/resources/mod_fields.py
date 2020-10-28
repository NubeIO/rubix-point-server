from flask_restful import fields

# TODO: move all to rest schemas

point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts': fields.String
}

point_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'reg': fields.Integer,
    'reg_length': fields.Integer,
    'type': fields.String,
    'enable': fields.Boolean,
    'write_value': fields.Float,
    'data_type': fields.String,
    'data_endian': fields.String,
    'data_round': fields.Integer,
    'data_offset': fields.Integer,
    'timeout': fields.Integer,
    'timeout_global': fields.Boolean,
    'prevent_duplicates': fields.Boolean,
    'created_on': fields.String,
    'updated_on': fields.String,
    'device_uuid': fields.String,
    'point_store': fields.Nested(point_store_fields),
}

device_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'enable': fields.Boolean,
    'type': fields.String,  # rtu or tcp
    'address': fields.Integer,  # 1,2,3
    'tcp_ip': fields.String,
    'tcp_port': fields.Integer,
    'ping_point_type': fields.String,  # for ping a reg to see if the device is online
    'ping_point_address': fields.Integer,
    'zero_mode': fields.Boolean,
    # These are 0-based addresses. so, the Modbus protocol address is equal to the Holding Register Offset minus one
    'timeout': fields.Integer,
    'timeout_global': fields.Boolean,  # true
    'fault': fields.Boolean,  # true
    'last_poll_timestamp': fields.String,
    'fault_timestamp': fields.String,
    'network_uuid': fields.String,
    'created_on': fields.String,
    'updated_on': fields.String,
    'points': fields.List(fields.Nested(point_fields)),
}

network_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'type': fields.String,  # rtu or tcp
    'enable': fields.Boolean,
    'timeout': fields.Integer,  # network time out
    'device_timeout_global': fields.Integer,  # device time out global setting
    'point_timeout_global': fields.Integer,  # point time out global setting
    'rtu_port': fields.String,  # /dev/ttyyUSB0
    'rtu_speed': fields.Integer,  # 9600
    'rtu_stop_bits': fields.Integer,  # 1
    'rtu_parity': fields.String,  # O E N Odd, Even, None
    'rtu_byte_size': fields.Integer,  # 5, 6, 7, or 8. This defaults to 8.
    'fault': fields.Boolean,  # true
    'last_poll_timestamp': fields.String,
    'fault_timestamp': fields.String,
    'created_on': fields.String,
    'updated_on': fields.String,
    'devices': fields.List(fields.Nested(device_fields)),
}
