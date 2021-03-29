from src.drivers.generic.resources.rest_schema.schema_generic_device import \
    generic_device_all_fields_with_children, generic_device_all_fields
from src.resources.rest_schema.schema_network import *

generic_network_all_attributes = {
    **deepcopy(network_all_attributes),
    'droplet_uuid': {
        'type': str,
        'required': True,
    },
}
generic_network_return_attributes = deepcopy(network_return_attributes)

generic_network_all_fields = {}
map_rest_schema(generic_network_return_attributes, generic_network_all_fields)
map_rest_schema(generic_network_all_attributes, generic_network_all_fields)

generic_network_all_fields_with_children = deepcopy(generic_network_all_fields)
generic_network_all_fields_with_children['devices'] = fields.List(fields.Nested(
    generic_device_all_fields_with_children))

generic_network_all_fields_without_point_children = deepcopy(generic_network_all_fields)
generic_network_all_fields_without_point_children['devices'] = fields.List(fields.Nested(generic_device_all_fields))
