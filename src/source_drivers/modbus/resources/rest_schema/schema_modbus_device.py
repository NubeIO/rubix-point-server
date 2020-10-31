from copy import deepcopy
from src.resources.rest_schema.schema_device import *

modbus_device_all_attributes = deepcopy(device_all_attributes)
modbus_device_all_attributes['type'] = {
    'type': str,
    'required': True,
}
modbus_device_all_attributes['address'] = {
    'type': int,
    'required': True,
}
modbus_device_all_attributes['tcp_ip'] = {
    'type': str,
}
modbus_device_all_attributes['tcp_port'] = {
    'type': int,
}
modbus_device_all_attributes['ping_point_type'] = {
    'type': str,
    'required': True,
}
modbus_device_all_attributes['ping_point_address'] = {
    'type': int,
    'required': True,
}
modbus_device_all_attributes['zero_mode'] = {
    'type': bool,
    'required': True,
}
modbus_device_all_attributes['timeout'] = {
    'type': float,
    'required': True,
}
modbus_device_all_attributes['timeout_global'] = {
    'type': bool,
    'required': True,
}
