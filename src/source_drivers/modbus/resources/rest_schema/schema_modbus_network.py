from src.resources.rest_schema.schema_network import *
from copy import deepcopy

modbus_network_all_attributes = deepcopy(network_all_attributes)
modbus_network_all_attributes['type'] = {
    'type': str,
    'required': True,
}
modbus_network_all_attributes['timeout'] = {
    'type': float,
    'required': True,
}
modbus_network_all_attributes['device_timeout_global'] = {
    'type': float,
    'required': True,
}
modbus_network_all_attributes['point_timeout_global'] = {
    'type': float,
    'required': True,
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
}
modbus_network_all_attributes['rtu_byte_size'] = {
    'type': int,
}
