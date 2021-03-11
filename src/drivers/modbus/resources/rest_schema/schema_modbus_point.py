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

modbus_poll_non_existing_attributes = {
    'network_rtu_port': {
        'type': str,
    },
    'network_rtu_speed': {
        'type': int,
    },
    'network_rtu_stop_bits': {
        'type': int,
    },
    'network_rtu_parity': {
        'type': str,
    },
    'network_rtu_byte_size': {
        'type': int,
    },
    'network_tcp_ip': {
        'type': str,
    },
    'network_tcp_port': {
        'type': int,
    },
    'network_type': {
        'type': str,
        'required': True
    },
    'network_timeout': {
        'type': int,
    },
    'device_address': {
        'type': int,
        'required': True
    },
    'device_zero_based': {
        'type': bool,
    },
    'point_register': {
        'type': int,
        'required': True
    },
    'point_register_length': {
        'type': int,
        'required': True
    },
    'point_function_code': {
        'type': str,
        'required': True
    },
    'point_write_value': {
        'type': float,
    },
    'point_data_type': {
        'type': str,
    },
    'point_data_endian': {
        'type': str,
    },
}

modbus_point_return_attributes = deepcopy(point_return_attributes)

modbus_point_all_fields = {}
map_rest_schema(modbus_point_return_attributes, modbus_point_all_fields)
map_rest_schema(modbus_point_all_attributes, modbus_point_all_fields)
