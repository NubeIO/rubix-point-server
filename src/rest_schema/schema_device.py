
INTERFACE_NAME = 'device'

device_all_attributes = {
    # 'uuid': {
    #     'type': str,
    #     'required': False,
    #     'help': '',
    # },
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

device_return_attributes = {}
