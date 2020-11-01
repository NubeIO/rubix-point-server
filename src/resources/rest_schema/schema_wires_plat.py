from src.resources.utils import map_rest_schema

wires_plat_all_attributes = {
    'device_id': {
        'type': str,
        'required': True,
        'help': '',
    },
    'device_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'client_id': {
        'type': str,
        'required': True,
        'help': '',
    },
    'client_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_id': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_address': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_city': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_state': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_zip': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_country': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_lat': {
        'type': str,
        'required': True,
        'help': '',
    },
    'site_lon': {
        'type': str,
        'required': True,
        'help': '',
    },
}

wires_plat_return_attributes = {
    'uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'created_on': {
        'type': str,
        'help': '',
    },
    'updated_on': {
        'type': str,
        'help': '',
    }
}

wires_plat_all_fields = {}
map_rest_schema(wires_plat_return_attributes, wires_plat_all_fields)
map_rest_schema(wires_plat_all_attributes, wires_plat_all_fields)
