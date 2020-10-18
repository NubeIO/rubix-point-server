

# TODO: need to make a class and private

attributes = {
    'name': 'name',
    'unit': 'unit',
    'timeout': 'timeout',
    'ping_address': 'ping_address',
    'ping_point_type':  'ping_point_type',
    'zeroMode': 'zeroMode'
}


THIS = 'device'
__interface_help_name = 'name'
interface_help = {
    'name': __interface_help_name,
    'type': int,
    'required': True,
    'help': f'/{THIS}, {__interface_help_name} is required'

}
__interface_help_unit = 'unit'
interface_unit = {
    'unit': 'unit',
    'type': str,
    'required': False,
    'help': f'/{THIS}  is optional'

}
