# TODO: need to make a class and private

# TODO: need to add in more things
# write_ok, fault, last_poll_timestamp

points_attributes = {
    'mod_point_uuid': 'mod_point_uuid',
    'mod_point_name': 'mod_point_name',
    'mod_point_reg': 'mod_point_reg',
    'mod_point_reg_length': 'mod_point_reg_length',
    'mod_point_type': 'mod_point_type',
    'mod_point_enable': 'mod_point_enable',
    'mod_point_write_value': 'mod_point_write_value',
    'mod_point_data_type': 'mod_point_data_type',
    'mod_point_data_endian': 'mod_point_data_endian',
    'mod_point_data_round': 'mod_point_data_round',
    'mod_point_data_offset': 'mod_point_data_offset',
    'mod_point_timeout': 'mod_point_timeout',
    'mod_point_timeout_global': 'mod_point_timeout_global',
    'mod_point_prevent_duplicates': 'mod_point_prevent_duplicates',
    'mod_device_uuid': 'mod_device_uuid',
    # 'mod_point_write_ok': 'mod_point_write_ok',
    # 'mod_point_fault': 'mod_point_fault',
    # 'mod_point_last_poll_timestamp': 'mod_point_last_poll_timestamp',

}



THIS = 'point'
_interface_help_name = 'mod_point_name'
interface_name = {
    'name': _interface_help_name,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_name} is required'

}
_interface_help_reg = 'mod_point_reg'
interface_reg = {
    'name': _interface_help_reg,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_reg} is required'

}
_interface_help_reg_length = 'mod_point_reg_length'
interface_reg_length = {
    'name': _interface_help_reg_length,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_reg_length} is required'

}
_interface_help_point_type = 'mod_point_type'
interface_point_type = {
    'name': _interface_help_point_type,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_type} is required'

}
_interface_help_point_enable = 'mod_point_enable'
interface_point_enable = {
    'name': _interface_help_point_enable,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_enable} is required'

}
_interface_help_point_write_value = 'mod_point_write_value'
interface_point_write_value = {
    'name': _interface_help_point_write_value,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_write_value} is required'

}
_interface_help_point_data_type = 'mod_point_data_type'
interface_point_data_type = {
    'name': _interface_help_point_data_type,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_data_type} is required'

}
_interface_help_point_data_endian = 'mod_point_data_endian'
interface_point_data_endian = {
    'name': _interface_help_point_data_endian,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_data_endian} is required'

}
_interface_help_point_data_offset = 'mod_point_data_offset'
interface_point_data_offset = {
    'name': _interface_help_point_data_offset,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_data_offset} is required'

}
_interface_help_point_data_round = 'mod_point_data_round'
interface_point_data_round = {
    'name': _interface_help_point_data_round,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_data_round} is required'

}
_interface_help_point_timeout = 'mod_point_timeout'
interface_point_timeout = {
    'name': _interface_help_point_timeout,
    'type': int,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_timeout} is required'

}

_interface_help_point_timeout_global = 'mod_point_timeout_global'
interface_point_timeout_global = {
    'name': _interface_help_point_timeout_global,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_timeout_global} is required'

}

_interface_help_point_point_prevent_duplicates = 'mod_point_prevent_duplicates'
interface_point_prevent_duplicates = {
    'name': _interface_help_point_point_prevent_duplicates,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_point_prevent_duplicates} is required'

}

_interface_help_point_prevent_duplicates_global = 'mod_point_prevent_duplicates_global'
interface_point_prevent_duplicates_global = {
    'name': _interface_help_point_prevent_duplicates_global,
    'type': bool,
    'required': True,
    'help': f'{THIS}, {_interface_help_point_prevent_duplicates_global} is required'

}
_interface_help_device_uuid = 'mod_device_uuid'
interface_interface_help_device_uuid = {
    'name': _interface_help_device_uuid,
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_device_uuid} is required'

}
