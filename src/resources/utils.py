from distutils.util import strtobool

from flask_restful import fields
from flask_restful import marshal
from rubix_http.exceptions.exception import BadDataException


def model_network_marshaller(data: any, args: dict, base_fields: dict, children_without_point_fields: dict,
                             children_fields: dict):
    with_children = False
    points = False
    try:
        if 'with_children' in args:
            with_children = bool(strtobool(args['with_children']))
        if 'points' in args:
            points = bool(strtobool(args['points']))
    except Exception:
        raise BadDataException('Invalid query string')

    if with_children:
        if points:
            return marshal(data, children_fields)
        else:
            return marshal(data, children_without_point_fields)
    else:
        return marshal(data, base_fields)


def model_marshaller_with_children(data: any, args: dict, base_fields: dict, children_fields: dict):
    with_children = False
    if 'with_children' in args:
        try:
            with_children = bool(strtobool(args['with_children']))
        except Exception:
            raise BadDataException('Invalid query string')

    if with_children:
        return marshal(data, children_fields)
    else:
        return marshal(data, base_fields)


def get_field_type(attr_type):
    if attr_type == int:
        return fields.Integer()
    elif attr_type == str:
        return fields.String()
    elif attr_type == bool:
        return fields.Boolean()
    elif attr_type == float:
        return fields.Float()


def map_rest_schema(schema, resource_fields):
    """
    Adds schema dict marshaled data to resource_fields dict
    """
    for attr in schema:
        # hack fix... change to make fields primary thing and switch get_field_type to return opposite
        if not isinstance(schema[attr]['type'], fields.Raw):
            resource_fields[attr] = get_field_type(schema[attr]['type'])
        else:
            resource_fields[attr] = schema[attr]['type']
        if schema[attr].get('nested', False):
            resource_fields[attr].__init__(attribute=schema[attr]['dict'])
