

# TODO: need to make a class and private

attributes = {
    'mod_device_uuid': 'mod_device_uuid',
    'mod_device_name': 'mod_device_name',
    'mod_device_ip': 'mod_device_ip',
    'mod_device_port': 'mod_device_port',
    'ping_point_type':  'ping_point_type',
    'zeroMode': 'zeroMode'
}



THIS = 'device'
_interface_help_name = 'mod_device_name'
interface_name = {
    'name': _interface_help_name,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_name} is required'

}
_interface_help_ip = 'mod_device_ip'
interface_ip = {
    'name': _interface_help_ip,
    'type': str,
    'required': False,
    'help': f'{THIS}, {_interface_help_name} is optional'

}

_interface_help_port = 'mod_device_port'
interface_port = {
    'name': _interface_help_port,
    'type': int,
    'required': False,
    'help': f'{THIS}, {_interface_help_name} is optional'

}

