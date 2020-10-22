

INTERFACE_NAME = 'network'

network_attributes = {
    'network_uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'network_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'network_enable': {
        'type': bool,
        'required': True,
        'help': '',
    },
}