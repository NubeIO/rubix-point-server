from copy import deepcopy

from src.resources.rest_schema.schema_point import *

generic_point_all_attributes = deepcopy(point_all_attributes)
generic_point_all_attributes['disable_mqtt'] = {
    'type': bool
}
generic_point_all_attributes['type'] = {
    'type': str,
    'nested': True,
    'dict': 'type.name'
}
generic_point_all_attributes['unit'] = {
    'type': str,
}

generic_point_return_attributes = deepcopy(point_return_attributes)
generic_point_all_fields = {}
map_rest_schema(generic_point_all_attributes, generic_point_all_fields)
map_rest_schema(generic_point_return_attributes, generic_point_all_fields)
