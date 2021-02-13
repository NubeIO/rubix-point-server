from src.resources.rest_schema.schema_device import *

mp_gbp_mapping_attributes = {
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

mp_gbp_mapping_fields = {}
map_rest_schema(mp_gbp_mapping_attributes, mp_gbp_mapping_fields)
