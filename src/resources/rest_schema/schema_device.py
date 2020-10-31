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
}

device_return_attributes = {
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
    }
}

device_all_fields = {}
map_rest_schema(device_return_attributes, device_all_fields)
map_rest_schema(device_all_attributes, device_all_fields)
