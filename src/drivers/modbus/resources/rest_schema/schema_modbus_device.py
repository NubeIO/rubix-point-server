from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_fields
from src.resources.rest_schema.schema_device import *

modbus_device_all_attributes = deepcopy(device_all_attributes)
modbus_device_all_attributes['address'] = {
    'type': int,
    'required': True,
}
modbus_device_all_attributes['tcp_ip'] = {
    'type': str,
}
modbus_device_all_attributes['tcp_port'] = {
    'type': int,
}
modbus_device_all_attributes['zero_based'] = {
    'type': bool,
}
modbus_device_all_attributes['ping_point'] = {
    'type': str,
}
modbus_device_all_attributes['timeout'] = {
    'type': int,
}
modbus_device_all_attributes['polling_interval_runtime'] = {
    'type': int,
}
modbus_device_all_attributes['point_interval_ms_between_points'] = {
    'type': int,
}

modbus_device_return_attributes = deepcopy(device_return_attributes)
modbus_device_return_attributes['type'] = {
    'type': str,
    'nested': True,
    'dict': 'type.name'
}

modbus_device_all_fields = {}
map_rest_schema(modbus_device_return_attributes, modbus_device_all_fields)
map_rest_schema(modbus_device_all_attributes, modbus_device_all_fields)

modbus_device_all_fields_with_children = deepcopy(modbus_device_all_fields)
modbus_device_all_fields_with_children.update(device_all_fields_with_children_base)
modbus_device_all_fields_with_children['points'] = fields.List(fields.Nested(modbus_point_all_fields))
