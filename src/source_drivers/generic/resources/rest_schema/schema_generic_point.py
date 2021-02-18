from collections import OrderedDict
from copy import deepcopy

from src.resources.rest_schema.schema_point import *

priority_array_write_fields = OrderedDict({
    '_1': fields.Float,
    '_2': fields.Float,
    '_3': fields.Float,
    '_4': fields.Float,
    '_5': fields.Float,
    '_6': fields.Float,
    '_7': fields.Float,
    '_8': fields.Float,
    '_9': fields.Float,
    '_10': fields.Float,
    '_11': fields.Float,
    '_12': fields.Float,
    '_13': fields.Float,
    '_14': fields.Float,
    '_15': fields.Float,
    '_16': fields.Float,
})

generic_point_all_attributes = deepcopy(point_all_attributes)
generic_point_all_attributes['type'] = {
    'type': str,
    'nested': True,
    'dict': 'type.name'
}
generic_point_all_attributes['unit'] = {
    'type': str,
}

generic_point_return_attributes = deepcopy(point_return_attributes)
generic_point_return_attributes['priority_array_write'] = {
    'type': fields.Nested(priority_array_write_fields),
}
generic_point_all_fields = {}
map_rest_schema(generic_point_return_attributes, generic_point_all_fields)
map_rest_schema(generic_point_all_attributes, generic_point_all_fields)
