from src.resources.utils import map_rest_schema

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
    'value': {
        'type': float,
        'nested': True,
        'dict': 'point_store.value',
    },
    'value_array': {
        'type': str,
        'nested': True,
        'dict': 'point_store.value_array',
    },
    'fault': {
        'type': bool,
        'nested': True,
        'dict': 'point_store.fault',
    },
    'last_poll_timestamp': {
        'type': str,
        'nested': True,
        'dict': 'point_store.ts',
    },
}

point_all_fields = {}
map_rest_schema(point_return_attributes, point_all_fields)
map_rest_schema(point_all_attributes, point_all_fields)
