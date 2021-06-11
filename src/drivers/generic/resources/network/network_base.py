import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic.models.network import GenericNetworkModel
from src.drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_attributes, \
    generic_network_all_fields, generic_network_all_fields_with_children, \
    generic_network_all_fields_without_point_children
from src.resources.utils import model_network_marshaller


def generic_network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, generic_network_all_fields,
                                    generic_network_all_fields_without_point_children,
                                    generic_network_all_fields_with_children)


class GenericNetworkBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_network_all_attributes:
        parser.add_argument(attr,
                            type=generic_network_all_attributes[attr].get('type'),
                            required=generic_network_all_attributes[attr].get('required', False),
                            help=generic_network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network(data):
        uuid: str = shortuuid.uuid()
        network: GenericNetworkModel = GenericNetworkModel(uuid=uuid, **data)
        network.save_to_db()
        return network
