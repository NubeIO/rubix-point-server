from src.rest_schema.schema_network import *

network_attributes['mod_network_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
network_attributes['mod_network_timeout'] = {
    'type': int,
    'required': True,
    'help': '',
}
network_attributes['mod_network_device_timeout_global'] = {
    'type': int,
    'required': True,
    'help': '',
}
network_attributes['mod_network_point_timeout_global'] = {
    'type': int,
    'required': True,
    'help': '',
}
network_attributes['mod_rtu_network_port'] = {
    'type': str,
    'required': False,
    'help': '',
}
network_attributes['mod_rtu_network_speed'] = {
    'type': str,
    'required': False,
    'help': '',
}
network_attributes['mod_rtu_network_stopbits'] = {
    'type': int,
    'required': False,
    'help': '',
}
network_attributes['mod_rtu_network_parity'] = {
    'type': str,
    'required': False,
    'help': '',
}
network_attributes['mod_rtu_network_bytesize'] = {
    'type': int,
    'required': False,
    'help': '',
}