from copy import deepcopy

from src.resources.rest_schema.schema_network import *

generic_network_all_attributes = deepcopy(network_all_attributes)

generic_network_return_attributes = deepcopy(network_return_attributes)

generic_network_all_fields = {}
map_rest_schema(generic_network_return_attributes, generic_network_all_fields)
map_rest_schema(generic_network_all_attributes, generic_network_all_fields)
