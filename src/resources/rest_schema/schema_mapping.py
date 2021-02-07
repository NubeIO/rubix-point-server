from src.resources.utils import map_rest_schema

bacnet_point_mapping_attributes = {
    'generic_point_uuid': {
        'type': str,
        'required': True,
    },
    'bacnet_point_uuid': {
        'type': str,
        'required': True,
    },
    'generic_point_name': {
        'type': str,
        'required': True,
    },
    'bacnet_point_name': {
        'type': str,
        'required': True,
    }
}

bacnet_point_mapping_fields = {}
map_rest_schema(bacnet_point_mapping_attributes, bacnet_point_mapping_fields)
