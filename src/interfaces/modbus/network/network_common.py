attributes = {
    'mod_network_uuid': 'mod_network_uuid',
    'mod_network_name': 'mod_network_name',
    'mod_network_type': 'mod_network_type',  # rtu or tcp
    'mod_network_enable': 'mod_network_enable',
    'mod_tcp_network_ip': 'mod_tcp_network_ip',
    'mod_tcp_network_port': 'mod_tcp_network_port',
    'mod_ping_point_type': 'mod_ping_point_type',  # for ping a reg to see if the device is online
    'mod_ping_point_address': 'mod_ping_point_address',
    'mod_network_zero_mode': 'mod_network_zero_mode',  # These are 0-based addresses. Therefore, the Modbus protocol address is equal to the Holding Register Offset minus one
    'mod_network_device_timeout': 'mod_network_device_timeout',
    'mod_network_device_timeout_global': 'mod_network_device_timeout_global', # true
    'mod_rtu_network_port': 'mod_rtu_network_port', # /dev/ttyyUSB0
    'mod_rtu_network_speed': 'mod_rtu_network_speed', # 9600
    'mod_rtu_network_stopbits': 'mod_rtu_network_stopbits',
    'mod_rtu_network_parity': 'mod_rtu_network_parity', # O E N Odd, Even, None
    'mod_rtu_network_bytesize': 'mod_rtu_network_bytesize'  # 5, 6, 7, or 8. This defaults to 8.
}

common_network_enable = {
    "enable": "enable",
    "disable": "disable",
}
