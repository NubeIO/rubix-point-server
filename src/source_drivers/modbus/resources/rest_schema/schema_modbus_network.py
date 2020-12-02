from copy import deepcopy

from src.resources.rest_schema.schema_network import *
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_fields

modbus_network_all_attributes = deepcopy(network_all_attributes)
modbus_network_all_attributes['type'] = {
    'type': str,
    'required': True,
    'nested': True,
    'dict': 'type.name'
}
modbus_network_all_attributes['timeout'] = {
    'type': float,
}
modbus_network_all_attributes['device_timeout_global'] = {
    'type': float,
}
modbus_network_all_attributes['point_timeout_global'] = {
    'type': float,
}
modbus_network_all_attributes['rtu_port'] = {
    'type': str,
}
modbus_network_all_attributes['rtu_speed'] = {
    'type': int,
}
modbus_network_all_attributes['rtu_stop_bits'] = {
    'type': int,
}
modbus_network_all_attributes['rtu_parity'] = {
    'type': str,
    'nested': True,
    'dict': 'rtu_parity.name'
}
modbus_network_all_attributes['rtu_byte_size'] = {
    'type': int,
}

modbus_network_return_attributes = deepcopy(network_return_attributes)
modbus_network_return_attributes['devices'] = {
    'type': fields.List(fields.Nested(modbus_device_all_fields))
}

modbus_network_all_fields = {}
map_rest_schema(modbus_network_return_attributes, modbus_network_all_fields)
map_rest_schema(modbus_network_all_attributes, modbus_network_all_fields)
