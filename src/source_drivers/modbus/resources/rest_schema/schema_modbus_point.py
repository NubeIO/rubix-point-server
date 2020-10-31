from flask_restful import fields

from src.resources.rest_schema.schema_point import *
from copy import deepcopy

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
modbus_point_all_attributes['write_value'] = {
    'type': float,
    'required': False,
}
modbus_point_all_attributes['data_type'] = {
    'type': str,
    'required': True,
}
modbus_point_all_attributes['data_endian'] = {
    'type': str,
    'required': True,
}
modbus_point_all_attributes['data_round'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['data_offset'] = {
    'type': int,
    'required': True,
}
modbus_point_all_attributes['timeout'] = {
    'type': float,
    'required': True,
}
modbus_point_all_attributes['timeout_global'] = {
    'type': bool,
    'required': True,
}

modbus_point_return_attributes = {
    'uuid': {
        'type': str,
    },
    'driver': {
        'type': str,
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    },
}

point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_array': fields.String,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts': fields.String
}

modbus_point_all_fields = {}
map_rest_schema(modbus_point_return_attributes, modbus_point_all_fields)
map_rest_schema(modbus_point_all_attributes, modbus_point_all_fields)
modbus_point_all_fields['point_store'] = fields.Nested(point_store_fields)
