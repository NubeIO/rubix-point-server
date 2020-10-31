from src.resources.utils import map_rest_schema

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
    }
}

network_all_fields = {}
map_rest_schema(network_return_attributes, network_all_fields)
map_rest_schema(network_all_attributes, network_all_fields)
