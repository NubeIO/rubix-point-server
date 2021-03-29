from src.drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_fields_with_children
from src.resources.rest_schema.schema_network import *

generic_network_droplet_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
    'type': {
        'type': str,
        'nested': True,
        'required': True,
        'dict': 'type.name'
    }
}
generic_network_droplet_return_attributes = {
    'uuid': {
        'type': str,
    },
}

generic_network_droplet_all_fields = {}
map_rest_schema(generic_network_droplet_all_attributes, generic_network_droplet_all_fields)
map_rest_schema(generic_network_droplet_return_attributes, generic_network_droplet_all_fields)

generic_network_droplet_all_fields_with_children = deepcopy(generic_network_droplet_all_fields)
generic_network_droplet_all_fields_with_children['networks'] = fields.List(
    fields.Nested(generic_network_all_fields_with_children))
