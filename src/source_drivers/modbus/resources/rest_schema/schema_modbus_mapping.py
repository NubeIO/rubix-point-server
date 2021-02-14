from src.resources.rest_schema.schema_device import *

mapping_mp_gbp_attributes = {
    'modbus_point_uuid': {
        'type': str,
        'required': True,
    },
    'generic_point_uuid': {
        'type': str,
    },
    'bacnet_point_uuid': {
        'type': str,
    },
    'modbus_point_name': {
        'type': str,
    },
    'generic_point_name': {
        'type': str,
    },
    'bacnet_point_name': {
        'type': str,
    },
}

mapping_mp_gbp_return_attributes = {
    'uuid': {
        'type': str,
    },
}

mapping_mp_gbp_all_fields = {}
map_rest_schema(mapping_mp_gbp_return_attributes, mapping_mp_gbp_all_fields)
map_rest_schema(mapping_mp_gbp_attributes, mapping_mp_gbp_all_fields)
