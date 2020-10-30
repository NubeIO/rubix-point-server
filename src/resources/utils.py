from flask_restful import fields


def getFieldType(attr_type):
    if attr_type == int:
        return fields.Integer()
    elif attr_type == str:
        return fields.String()
    elif attr_type == bool:
        return fields.Boolean()
    elif attr_type == float:
        return fields.Float()


def mapRestSchema(schema, resource_fields):
    """
    Adds schema dict marshaled data to resource_fields dict
    """
    for attr in schema:
        resource_fields[attr] = getFieldType(schema[attr]['type'])
        if schema[attr].get('nested', False):
            resource_fields[attr].__init__(attribute=schema[attr]['dict'])
