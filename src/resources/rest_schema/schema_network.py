from flask_restful import fields

from src.resources.utils import map_rest_schema
from src.resources.rest_schema.schema_device import device_all_fields

network_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
    'enable': {
        'type': bool,
        'required': True,
    },
    'fault': {
        'type': bool,
    },
    'history_enable': {
        'type': bool,
    },
}

network_return_attributes = {
    'uuid': {
        'type': str,
    },
    'driver': {
        'type': str
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    },
    'devices': {
        'type': fields.List(fields.Nested(device_all_fields))
    }
}

network_all_fields = {}
map_rest_schema(network_return_attributes, network_all_fields)
map_rest_schema(network_all_attributes, network_all_fields)
