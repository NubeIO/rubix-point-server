
INTERFACE_NAME = 'device'

device_all_attributes = {
    'name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'network_uuid': {
        'type': str,
        'required': True,
        'help': '',
    },
    'enable': {
        'type': bool,
        'required': False,
        'help': '',
    },
    'fault': {
        'type': bool,
        'required': False,
        'help': '',
    },
    'fault_timestamp': {
        'type': int,
        'required': False,
        'help': '',
    },
}

device_return_attributes = {
    'uuid': {
        'type': str,
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
