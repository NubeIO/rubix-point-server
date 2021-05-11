from src.drivers.generic.resources.rest_schema.schema_generic_point import generic_point_all_fields
from src.resources.rest_schema.schema_device import *

generic_device_all_attributes = deepcopy(device_all_attributes)
generic_device_return_attributes = deepcopy(device_return_attributes)
generic_device_return_attributes['tags'] = {
    'type': str,
}
generic_device_all_fields = {}
map_rest_schema(generic_device_return_attributes, generic_device_all_fields)
map_rest_schema(generic_device_all_attributes, generic_device_all_fields)

generic_device_all_fields_with_children = deepcopy(generic_device_all_fields)
generic_device_all_fields_with_children.update(device_all_fields_with_children_base)
generic_device_all_fields_with_children['points'] = fields.List(fields.Nested(generic_point_all_fields))
