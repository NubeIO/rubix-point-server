from copy import deepcopy

from src.resources.rest_schema.schema_point import *

modbus_point_all_attributes = deepcopy(point_all_attributes)
modbus_point_all_attributes['register'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['register_length'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['function_code'] = {
    'type': str,
    'required': True,
    'nested': True,
    'dict': 'function_code.name'
}
modbus_point_all_attributes['data_type'] = {
    'type': str,
    'nested': True,
    'dict': 'data_type.name'
}
modbus_point_all_attributes['data_endian'] = {
    'type': str,
    'nested': True,
    'dict': 'data_endian.name'
}
modbus_point_all_attributes['timeout'] = {
    'type': float,
}
modbus_point_all_attributes['timeout_global'] = {
    'type': bool,
}

modbus_point_return_attributes = deepcopy(point_return_attributes)

modbus_point_all_fields = {}
map_rest_schema(modbus_point_return_attributes, modbus_point_all_fields)
map_rest_schema(modbus_point_all_attributes, modbus_point_all_fields)
