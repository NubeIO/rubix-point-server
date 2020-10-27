# TODO: need to make a class and private

INTERFACE_NAME = 'point'

point_all_attributes = {
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
    'prevent_duplicates': {
        'type': bool,
        'required': False,
        'help': '',
    },

}

point_return_attributes = {
    'value': {
        'type': float,
        'nested': True,
        'dict': 'value.point_value',
        'help': ''
    },
    # 'write_ok': {
    #     'type': str,
    #     'help': '',
    # },
    'fault': {
        'type': bool,
        'nested': True,
        'dict': 'value.fault',
        'help': '',
    },
    'last_poll_timestamp': {
        'type': str,
        'help': '',
    },
}