import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.generic.models.network_droplet import GenericNetworkDropletModel
from src.drivers.generic.resources.rest_schema.schema_generic_network_drroplet import \
    generic_network_droplet_all_fields, generic_network_droplet_all_fields_with_children, \
    generic_network_droplet_all_attributes
from src.resources.utils import model_marshaller_with_children


def generic_network_droplet_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, generic_network_droplet_all_fields,
                                          generic_network_droplet_all_fields_with_children)


class GenericNetworkDropletBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in generic_network_droplet_all_attributes:
        parser.add_argument(attr,
                            type=generic_network_droplet_all_attributes[attr].get('type'),
                            required=generic_network_droplet_all_attributes[attr].get('required', False),
                            help=generic_network_droplet_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network_droplet(data):
        _uuid = str(uuid.uuid4())
        network_droplet: GenericNetworkDropletModel = GenericNetworkDropletModel(uuid=_uuid, **data)
        network_droplet.save_to_db()
        return network_droplet
