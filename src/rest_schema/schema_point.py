# TODO: need to make a class and private

INTERFACE_NAME = 'point'

point_all_attributes = {
    'point_uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'point_name': {
        'type': str,
        'required': True,
        'help': '',
    },
    'point_device_uuid': {
        'type': str,
        'required': False,
        'help': '',
    },
    'point_enable': {
        'type': bool,
        'required': True,
        'help': '',
    },
    'point_prevent_duplicates': {
        'type': bool,
        'required': False,
        'help': '',
    },

}

point_return_attributes = {
    'point_value': {
        'type': float,
        'nested': True,
        'dict': 'value.point_value',
        'help': ''
    },
    'point_write_ok': {
        'type': str,
        'help': '',
    },
    'point_fault': {
        'type': str,
        'help': '',
    },
    'point_last_poll_timestamp': {
        'type': str,
        'help': '',
    },
}