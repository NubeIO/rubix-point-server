

# TODO: need to make a class and private

THIS = 'device'

attributes = {
    'mod_device_uuid': 'mod_device_uuid',
    'mod_device_name': 'mod_device_name',
    'mod_device_enable': 'mod_device_enable',
    'mod_device_type': 'mod_network_type',  # rtu or tcp
    'mod_device_addr': 'mod_device_addr',  # 1,2,3
    'mod_tcp_device_ip': 'mod_tcp_device_ip',
    'mod_tcp_device_port': 'mod_tcp_device_port',
    'mod_ping_point_type': 'mod_ping_point_type',  # for ping a reg to see if the device is online
    'mod_ping_point_address': 'mod_ping_point_address',
    'mod_network_zero_mode': 'mod_network_zero_mode', # These are 0-based addresses. Therefore, the Modbus protocol address is equal to the Holding Register Offset minus one
    'mod_device_timeout': 'mod_device_timeout',
    'mod_device_timeout_global': 'mod_device_timeout_global',  # true

}
_interface_mod_device_name = 'mod_device_name'
interface_mod_device_name = {
    'name': _interface_mod_device_name,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_name} is required'

}
_interface_mod_device_enable = 'mod_device_enable'
interface_mod_device_enable = {
    'name': _interface_mod_device_enable,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_enable} is required'

}
_mod_mod_device_type = 'mod_device_type'
interface_mod_device_type = {
    'name': _mod_mod_device_type,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_mod_mod_device_type} is required'

}
_interface_mod_device_addr = 'mod_device_addr'
interface_mod_device_addr = {
    'name': _interface_mod_device_addr,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_addr} is required if its a tcp device'

}
_interface_mod_tcp_device_ip = 'mod_tcp_device_ip'
interface_mod_tcp_device_ip = {
    'name': _interface_mod_tcp_device_ip,
    'type': str,
    'required': False,
    'help': f'{THIS}, {_interface_mod_tcp_device_ip} is required if its a tcp device'

}
_interface_mod_tcp_device_port = 'mod_tcp_device_port'
interface_mod_tcp_device_port = {
    'name': _interface_mod_tcp_device_port,
    'type': int,
    'required': False,
    'help': f'{THIS}, {_interface_mod_tcp_device_port} is required'

}
_interface_mod_ping_point_type = 'mod_ping_point_type'
interface_mod_ping_point_type = {
    'name': _interface_mod_ping_point_type,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_mod_ping_point_type} is required'

}
_interface_mod_ping_point_address = 'mod_ping_point_address'
interface_mod_ping_point_address = {
    'name': _interface_mod_ping_point_address,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_ping_point_address} is required'

}
_interface_mod_device_zero_mode = 'mod_device_zero_mode'
interface_mod_device_zero_mode = {
    'name': _interface_mod_device_zero_mode,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_zero_mode} is required'

}
_interface_mod_device_timeout = 'mod_device_timeout'
interface_mod_device_timeout = {
    'name': _interface_mod_device_timeout,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_timeout} is required'

}
_interface_mod_device_timeout_global = 'mod_device_timeout_global'
interface_mod_device_timeout_global = {
    'name': _interface_mod_device_timeout_global,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_mod_device_timeout_global} is required'

}
