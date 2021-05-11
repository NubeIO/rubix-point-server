from copy import deepcopy

from flask_restful import fields

from src.resources.rest_schema.schema_point import point_all_fields
from src.resources.utils import map_rest_schema

device_all_attributes = {
    'network_uuid': {
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
    'fault': {
        'type': bool,
    },
    'history_enable': {
        'type': bool,
    },
    'tags': {
        'type': str
    }
}

device_return_attributes = {
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
    }
}

device_all_fields = {}
map_rest_schema(device_return_attributes, device_all_fields)
map_rest_schema(device_all_attributes, device_all_fields)

device_all_fields_with_children_base = {
    'points': fields.List(fields.Nested(point_all_fields))
}
device_all_fields_with_children = deepcopy(device_all_fields)
device_all_fields_with_children.update(device_all_fields_with_children_base)
