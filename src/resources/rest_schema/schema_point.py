INTERFACE_NAME = 'point'

point_all_attributes = {
    'name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'device_uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'enable': {
        'type': bool,
        'required': True,
        'help': '',
    },
    'history_enable': {
        'type': bool,
        'required': False,
        'help': '',
    },
    'history_type': {
        'type': str,
        'required': False,
        'help': '',
    },
    'history_interval': {
        'type': int,
        'required': False,
        'help': '',
    },
}

point_return_attributes = {
    'uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'value': {
        'type': float,
        'nested': True,
        'dict': 'point_store.value',
        'help': ''
    },
    'value_array': {
        'type': str,
        'nested': True,
        'dict': 'point_store.value_array',
        'help': ''
    },
    'fault': {
        'type': bool,
        'nested': True,
        'dict': 'point_store.fault',
        'help': '',
    },
    'last_poll_timestamp': {
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
