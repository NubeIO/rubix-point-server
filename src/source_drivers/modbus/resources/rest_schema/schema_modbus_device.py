from copy import deepcopy

from src.resources.rest_schema.schema_device import *
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields

modbus_device_all_attributes = deepcopy(device_all_attributes)
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
# modbus_device_all_attributes['ping_point_type'] = {
#     'type': str,
# }
# modbus_device_all_attributes['ping_point_address'] = {
#     'type': int,
# }
modbus_device_all_attributes['zero_based'] = {
    'type': bool,
}
modbus_device_all_attributes['timeout'] = {
    'type': float,
}
modbus_device_all_attributes['timeout_global'] = {
    'type': bool,
}

modbus_device_return_attributes = deepcopy(device_return_attributes)
modbus_device_return_attributes['points'] = {
    'type': fields.List(fields.Nested(modbus_point_all_fields))
}
modbus_device_return_attributes['type'] = {
    'type': str,
    'nested': True,
    'dict': 'type.name'
}

modbus_device_all_fields = {}
map_rest_schema(modbus_device_return_attributes, modbus_device_all_fields)
map_rest_schema(modbus_device_all_attributes, modbus_device_all_fields)
