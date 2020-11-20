from flask_restful import fields
from src.resources.utils import map_rest_schema

point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_array': fields.String,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts': fields.String
}

point_all_attributes = {
    'device_uuid': {
        'type': str,
        'required': True,
    },
    'name': {
        'type': str,
        'required': True,
    },
    'enable': {
        'type': bool,
        'required': True,
    },
    'history_enable': {
        'type': bool,
    },
    'history_type': {
        'type': str,
    },
    'history_interval': {
        'type': int,
    },
}

point_return_attributes = {
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
    'writable': {
        'type': bool,
    },
    'write_value': {
        'type': float,
    },
    'point_store': {
        'type': fields.Nested(point_store_fields),
    }
}

point_all_fields = {}
map_rest_schema(point_return_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)
