

INTERFACE_NAME = 'network'

network_all_attributes = {
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
    'enable': {
        'type': bool,
        'required': True,
        'help': '',
    },
}

network_return_attributes = {}
