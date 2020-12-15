from src.resources.rest_schema.schema_network import *
from src.source_drivers.generic.resources.rest_schema.schema_generic_device import \
    generic_device_all_fields_with_children

generic_network_all_attributes = deepcopy(network_all_attributes)

generic_network_return_attributes = deepcopy(network_return_attributes)

generic_network_all_fields = {}
map_rest_schema(generic_network_return_attributes, generic_network_all_fields)
map_rest_schema(generic_network_all_attributes, generic_network_all_fields)

generic_network_all_fields_with_children = deepcopy(generic_network_all_fields)
generic_network_all_fields_with_children.update(network_all_fields_with_children_base)
generic_network_all_fields_with_children['devices'] = fields.List(fields.Nested(
    generic_device_all_fields_with_children))
