from src.rest_schema.schema_point import *


point_attributes['mod_point_reg'] = {
    'type': int,
    'required': True,
    'help': '',
}
point_attributes['mod_point_reg_length'] = {
    'type': int,
    'required': True,
    'help': '',
}
point_attributes['mod_point_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
point_attributes['mod_point_write_value'] = {
    'type': int,
    'required': False,
    'help': '',
}
point_attributes['mod_point_data_type'] = {
    'type': str,
    'required': True,
    'help': '',
}
point_attributes['mod_point_data_endian'] = {
    'type': str,
    'required': True,
    'help': '',
}
point_attributes['mod_point_data_offset'] = {
    'type': int,
    'required': True,
    'help': '',
}
point_attributes['mod_point_data_round'] = {
    'type': int,
    'required': True,
    'help': '',
}
point_attributes['mod_point_timeout'] = {
    'type': int,
    'required': True,
    'help': '',
}
point_attributes['mod_point_timeout_global'] = {
    'type': bool,
    'required': True,
    'help': '',
}