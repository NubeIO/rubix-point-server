from copy import deepcopy
from src.rest_schema.schema_device import *

modbus_device_all_attributes = deepcopy(device_all_attributes)
modbus_device_all_attributes['mod_device_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_device_addr'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_tcp_device_ip'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_tcp_device_port'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_ping_point_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_ping_point_address'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_device_zero_mode'] = {
    'type': bool,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_device_timeout'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_device_timeout_global'] = {
    'type': bool,
    'required': True,
    'help': '',
}
modbus_device_all_attributes['mod_device_last_poll_timestamp'] = {
    'type': int,
    'required': False,
    'help': '',
}