from flask_restful import fields

point_fields = {
    'mod_point_uuid': fields.String,
    'mod_point_name': fields.String,
    'mod_point_reg': fields.Integer,
    'mod_point_reg_length': fields.Integer,
    'mod_point_type': fields.String,
    'mod_point_enable': fields.Boolean,
    'mod_point_write_value': fields.Integer,
    'mod_point_data_type': fields.String,
    'mod_point_data_endian': fields.String,
    'mod_point_data_round': fields.Integer,
    'mod_point_data_offset': fields.Integer,
    'mod_point_timeout': fields.Integer,
    'mod_point_timeout_global': fields.Boolean,
    'mod_point_prevent_duplicates': fields.Boolean,
    'mod_point_prevent_duplicates_global': fields.Boolean,
    'mod_point_write_ok': fields.Boolean,
    'mod_point_fault': fields.Boolean,
    'mod_point_last_poll_timestamp': fields.String,
    'mod_point_value': fields.Float,
    'mod_point_value_array': fields.String,
    'mod_device_uuid': fields.String,
}

device_fields = {
    'mod_device_uuid': fields.String,
    'mod_device_name': fields.String,
    'mod_device_enable': fields.Boolean,
    'mod_device_type': fields.String,  # rtu or tcp
    'mod_device_addr': fields.Integer,  # 1,2,3
    'mod_tcp_device_ip': fields.String,
    'mod_tcp_device_port': fields.Integer,
    'mod_ping_point_type': fields.String,  # for ping a reg to see if the device is online
    'mod_ping_point_address': fields.Integer,
    'mod_device_zero_mode': fields.Boolean,
    # These are 0-based addresses. so, the Modbus protocol address is equal to the Holding Register Offset minus one
    'mod_device_timeout': fields.Integer,
    'mod_device_timeout_global': fields.Boolean,  # true
    'mod_device_fault': fields.Boolean,  # true
    'mod_device_last_poll_timestamp': fields.String,
    'mod_device_fault_timestamp': fields.String,
    'mod_network_uuid': fields.String,
    'mod_points': fields.List(fields.Nested(point_fields)),
}

network_fields = {
    'mod_network_uuid': fields.String,
    'mod_network_name': fields.String,
    'mod_network_type': fields.String,  # rtu or tcp
    'mod_network_enable': fields.Boolean,
    'mod_network_timeout': fields.Integer,  # network time out
    'mod_network_device_timeout_global': fields.Integer,  # device time out global setting
    'mod_network_point_timeout_global': fields.Integer,  # point time out global setting
    'mod_rtu_network_port': fields.String,  # /dev/ttyyUSB0
    'mod_rtu_network_speed': fields.Integer,  # 9600
    'mod_rtu_network_stopbits': fields.Integer,  # 1
    'mod_rtu_network_parity': fields.String,  # O E N Odd, Even, None
    'mod_rtu_network_bytesize': fields.Integer,  # 5, 6, 7, or 8. This defaults to 8.
    'mod_network_fault': fields.Boolean,  # true
    'mod_network_last_poll_timestamp': fields.String,
    'mod_network_fault_timestamp': fields.String,
    'mod_devices': fields.List(fields.Nested(device_fields)),
}
