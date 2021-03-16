from collections import OrderedDict

from flask_restful import fields

from src.resources.utils import map_rest_schema

priority_array_write_fields = OrderedDict({
    '_1': fields.Float,
    '_2': fields.Float,
    '_3': fields.Float,
    '_4': fields.Float,
    '_5': fields.Float,
    '_6': fields.Float,
    '_7': fields.Float,
    '_8': fields.Float,
    '_9': fields.Float,
    '_10': fields.Float,
    '_11': fields.Float,
    '_12': fields.Float,
    '_13': fields.Float,
    '_14': fields.Float,
    '_15': fields.Float,
    '_16': fields.Float,
})

point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_original': fields.Float,
    'value_raw': fields.String,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts_value': fields.String,
    'ts_fault': fields.String
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
    'writable': {
        'type': bool,
    },
    'write_value': {
        'type': float,
    },
    'cov_threshold': {
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
    'tags': {
        'type': str
    }
}

point_return_attributes = {
    'uuid': {
        'type': str,
    },
    'driver': {
        'type': str,
        'nested': True,
        'dict': 'driver.name'
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    },
    'priority_array_write': {
        'type': fields.Nested(priority_array_write_fields),
    },
    'point_store': {
        'type': fields.Nested(point_store_fields),
    }
}

point_all_fields = {}
map_rest_schema(point_return_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)
