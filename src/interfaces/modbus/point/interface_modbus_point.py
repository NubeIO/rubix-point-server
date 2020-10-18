# TODO: need to make a class and private

attributes = {
    'mod_point_uuid': 'mod_point_uuid',
    'mod_point_name': 'mod_point_name',
    'mod_point_reg': 'mod_point_reg',
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
    'type': str,
    'required': True,
    'help': f'{THIS}, {_interface_help_reg} is required'

}
