from flask_restful import Resource, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_attributes, \
    generic_network_all_fields, generic_network_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def generic_network_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, generic_network_all_fields,
                                          generic_network_all_fields_with_children)


class GenericNetworkBase(Resource):
    parser = reqparse.RequestParser()
    for attr in generic_network_all_attributes:
        parser.add_argument(attr,
                            type=generic_network_all_attributes[attr].get('type'),
                            required=generic_network_all_attributes[attr].get('required', False),
                            help=generic_network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_network_model_obj(uuid, data):
        return GenericNetworkModel(uuid=uuid, **data)

    @staticmethod
    def add_network(uuid, data):
        try:
            network = GenericNetworkBase.create_network_model_obj(uuid, data)
            network.save_to_db()
            return network
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
