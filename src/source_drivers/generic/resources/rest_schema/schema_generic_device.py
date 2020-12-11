from copy import deepcopy

from src.resources.rest_schema.schema_device import *

generic_device_all_attributes = deepcopy(device_all_attributes)

generic_device_return_attributes = deepcopy(device_return_attributes)

generic_device_all_fields = {}
map_rest_schema(generic_device_return_attributes, generic_device_all_fields)
map_rest_schema(generic_device_all_attributes, generic_device_all_fields)
