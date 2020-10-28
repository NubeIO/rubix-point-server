

INTERFACE_NAME = 'network'

network_all_attributes = {
    'name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'enable': {
        'type': bool,
        'required': True,
        'help': '',
    },
}

network_return_attributes = {
    'uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'created_on': {
        'type': str,
        'help': '',
    },
    'updated_on': {
        'type': str,
        'help': '',
    }
}
