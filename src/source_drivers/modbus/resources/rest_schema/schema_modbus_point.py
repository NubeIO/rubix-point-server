from src.rest_schema.schema_point import *
from copy import deepcopy

modbus_point_all_attributes = deepcopy(point_all_attributes)
modbus_point_all_attributes['reg'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['reg_length'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['type'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['data_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['data_endian'] = {
    'type': str,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['data_offset'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['data_round'] = {
    'type': int,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['write_value'] = {
    'type': float,
    'required': False,
    'help': '',
}
modbus_point_all_attributes['timeout'] = {
    'type': float,
    'required': True,
    'help': '',
}
modbus_point_all_attributes['timeout_global'] = {
    'type': bool,
    'required': True,
    'help': '',
}