
INTERFACE_NAME = 'device'

device_all_attributes = {
    'device_uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'device_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'device_network_uuid': {
        'type': str,
        'required': True,
        'help': '',
    },
    'device_enable': {
        'type': bool,
        'required': False,
        'help': '',
    },
    'device_fault': {
        'type': bool,
        'required': False,
        'help': '',
    },
    'device_fault_timestamp': {
        'type': int,
        'required': False,
        'help': '',
    },
}

device_return_attributes = {}
