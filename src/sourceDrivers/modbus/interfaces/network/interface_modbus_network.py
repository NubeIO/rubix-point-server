attributes = {
    'mod_network_uuid': 'mod_network_uuid',
    'mod_network_name': 'mod_network_name',
    'mod_network_type': 'mod_network_type',  # rtu or tcp
    'mod_network_enable': 'mod_network_enable',
    'mod_network_timeout': 'mod_network_timeout',  # network time out
    'mod_network_device_timeout_global': 'mod_network_device_timeout_global',  # device time out global setting
    'mod_network_point_timeout_global': 'mod_network_point_timeout_global',  # point time out global setting
    'mod_rtu_network_port': 'mod_rtu_network_port',  # /dev/ttyyUSB0
    'mod_rtu_network_speed': 'mod_rtu_network_speed',  # 9600
    'mod_rtu_network_stopbits': 'mod_rtu_network_stopbits',  # 1
    'mod_rtu_network_parity': 'mod_rtu_network_parity',  # O E N Odd, Even, None
    'mod_rtu_network_bytesize': 'mod_rtu_network_bytesize',  # 5, 6, 7, or 8. This defaults to 8.

}

THIS = 'network'
_interface_help_name = 'mod_network_name'
interface_mod_network_name = {
    'name': _interface_help_name,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_name} is required'

}
_mod_network_type = 'mod_network_type'
interface_mod_network_type = {
    'name': _mod_network_type,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_mod_network_type} is required'

}
_interface_mod_network_enable = 'mod_network_enable'
interface_mod_network_enable= {
    'name': _interface_mod_network_enable,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_mod_network_enable} is required'

}

_interface_mod_network_timeout = 'mod_network_timeout'
interface_mod_network_timeout = {
    'name': _interface_mod_network_timeout,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_network_timeout} is required'

}
_interface_mod_network_device_timeout_global = 'mod_network_device_timeout_global'
interface_mod_network_device_timeout_global = {
    'name': _interface_mod_network_device_timeout_global,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_network_device_timeout_global} is required'

}
_interface_mod_network_point_timeout_global = 'mod_network_point_timeout_global'
interface_mod_network_point_timeout_global = {
    'name': _interface_mod_network_point_timeout_global,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_network_point_timeout_global} is required'

}
_interface_mod_rtu_network_port = 'mod_rtu_network_port'
interface_mod_rtu_network_port = {
    'name': _interface_mod_rtu_network_port,
    'type': str,
    'required': False,
    'help': f'{THIS}, {_interface_mod_rtu_network_port} is required'

}
_interface_mod_rtu_network_speed = 'mod_rtu_network_speed'
interface_mod_rtu_network_speed = {
    'name': _interface_mod_rtu_network_speed,
    'type': str,
    'required': False,
    'help': f'{THIS}, {_interface_mod_rtu_network_speed} is required'

}
_interface_mod_rtu_network_stopbits = 'mod_rtu_network_stopbits'
interface_mod_rtu_network_stopbits = {
    'name': _interface_mod_rtu_network_stopbits,
    'type': int,
    'required': False,
    'help': f'{THIS}, {_interface_mod_rtu_network_stopbits} is required'

}
_interface_mod_rtu_network_parity = 'mod_rtu_network_parity'
interface_mod_rtu_network_parity = {
    'name': _interface_mod_rtu_network_parity,
    'type': str,
    'required': False,
    'help': f'{THIS}, {_interface_mod_rtu_network_parity} is required'

}
_interface_mod_rtu_network_bytesize = 'mod_rtu_network_bytesize'
interface_mod_rtu_network_bytesize = {
    'name': _interface_mod_rtu_network_bytesize,
    'type': int,
    'required': False,
    'help': f'{THIS}, {_interface_mod_rtu_network_bytesize} is required'

}
