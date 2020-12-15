from flask_restful import marshal_with, abort, reqparse

from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.network.network_base import GenericNetworkBase
from src.source_drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_fields, \
    generic_network_all_attributes


class GenericNetworkSingular(GenericNetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_network_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_network_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(generic_network_all_fields)
    def get(cls, uuid):
        network = GenericNetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Generic Network not found')
        return network

    @classmethod
    @marshal_with(generic_network_all_fields)
    def put(cls, uuid):
        data = GenericNetworkSingular.parser.parse_args()
        network = GenericNetworkModel.find_by_uuid(uuid)
        if network is None:
            return cls.add_network(uuid, data)
        else:
            try:
                network.update(**data)
                return GenericNetworkModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    @marshal_with(generic_network_all_fields)
    def patch(cls, uuid):
        data = GenericNetworkSingular.patch_parser.parse_args()
        network = GenericNetworkModel.find_by_uuid(uuid)
        if network is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                network.update(**data)
                return GenericNetworkModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        network = GenericNetworkModel.find_by_uuid(uuid)
        if network is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            network.delete_from_db()
            return '', 204
