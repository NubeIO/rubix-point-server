from copy import deepcopy

from src.resources.rest_schema.schema_point import *

generic_point_all_attributes = deepcopy(point_all_attributes)

generic_point_return_attributes = deepcopy(point_return_attributes)

generic_point_all_fields = {}
map_rest_schema(generic_point_return_attributes, generic_point_all_fields)
map_rest_schema(generic_point_all_attributes, generic_point_all_fields)
