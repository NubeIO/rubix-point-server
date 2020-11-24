from copy import deepcopy
from src.resources.rest_schema.schema_point import *

modbus_point_all_attributes = deepcopy(point_all_attributes)
modbus_point_all_attributes['reg'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['reg_length'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['type'] = {
    'type': str,
    'required': True,
}
modbus_point_all_attributes['data_type'] = {
    'type': str,
    'required': True,
}
modbus_point_all_attributes['data_endian'] = {
    'type': str,
    'required': False,
}
modbus_point_all_attributes['data_round'] = {
    'type': int,
    'required': False,
}
modbus_point_all_attributes['data_offset'] = {
    'type': int,
    'required': False,
}
modbus_point_all_attributes['timeout'] = {
    'type': float,
    'required': False,
}
modbus_point_all_attributes['timeout_global'] = {
    'type': bool,
    'required': False,
}

modbus_point_return_attributes = deepcopy(point_return_attributes)

modbus_point_all_fields = {}
map_rest_schema(modbus_point_return_attributes, modbus_point_all_fields)
map_rest_schema(modbus_point_all_attributes, modbus_point_all_fields)
