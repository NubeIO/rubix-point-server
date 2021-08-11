import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.models.network.model_network import NetworkModel
from src.resources.rest_schema.schema_network import network_all_attributes, network_all_fields, \
    network_all_fields_with_children, network_all_fields_without_point_children
from src.resources.utils import model_network_marshaller


def network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, network_all_fields, network_all_fields_without_point_children,
                                    network_all_fields_with_children)


class NetworkBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in network_all_attributes:
        parser.add_argument(attr,
                            type=network_all_attributes[attr].get('type'),
                            required=network_all_attributes[attr].get('required', False),
                            help=network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network(data):
        uuid: str = shortuuid.uuid()
        network: NetworkModel = NetworkModel(uuid=uuid, **data)
        network.save_to_db()
        return network
