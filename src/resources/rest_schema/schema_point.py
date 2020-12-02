from flask_restful import fields

from src.resources.utils import map_rest_schema

point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_original': fields.Float,
    'value_raw': fields.String,
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
        'nested': True,
        'dict': 'history_type.name'
    },
    'history_interval': {
        'type': int,
    },
    'cov_threshold': {
        'type': float,
    },
    'write_value': {
        'type': float,
    },
    'value_round': {
        'type': int,
    },
    'value_offset': {
        'type': float,
    },
    'value_operation': {
        'type': str,
        'nested': True,
        'dict': 'value_operation.name'
    },
    'input_min': {
        'type': float,
    },
    'input_max': {
        'type': float,
    },
    'scale_min': {
        'type': float,
    },
    'scale_max': {
        'type': float,
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
    'point_store': {
        'type': fields.Nested(point_store_fields),
    }
}

point_all_fields = {}
map_rest_schema(point_return_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)
