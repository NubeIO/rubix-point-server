from src.resources.rest_schema.schema_device import *

mapping_mp_gbp_attributes = {
    'point_uuid': {
        'type': str,
        'required': True,
    },
    'mapped_point_uuid': {
        'type': str,
        'required': True,
    },
    'point_name': {
        'type': str,
        'required': True,
    },
    'mapped_point_name': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'dict': 'type.name',
        'required': True,
    },
    'mapping_state': {
        'type': str,
        'nested': True,
        'dict': 'mapping_state.name',
        'required': True,
    },
}

mapping_mp_gbp_uuid_attributes = {
    'point_uuid': {
        'type': str,
        'required': True,
    },
    'mapped_point_uuid': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'dict': 'type.name',
        'required': True,
    },
}

mapping_mp_gbp_name_attributes = {
    'point_name': {
        'type': str,
        'required': True,
    },
    'mapped_point_name': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'dict': 'type.name',
        'required': True,
    },
}

mapping_mp_gbp_patch_attributes = {
    'point_uuid': {
        'type': str,
        'required': True,
    },
    'mapped_point_uuid': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'dict': 'type.name',
        'required': True,
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
