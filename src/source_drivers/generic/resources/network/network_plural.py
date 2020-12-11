import uuid
from flask_restful import marshal_with

from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.network.network_base import GenericNetworkBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_fields


class GenericNetworkPlural(GenericNetworkBase):

    @classmethod
    @marshal_with(generic_network_all_fields)
    def get(cls):
        return GenericNetworkModel.query.all()

    @classmethod
    @marshal_with(generic_network_all_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = GenericNetworkPlural.parser.parse_args()
        return cls.add_network(_uuid, data)
