from flask_restful import abort, reqparse
from flask_restful.reqparse import request

from src.source_drivers.generic.models.network import GenericNetworkModel
from src.source_drivers.generic.resources.network.network_base import GenericNetworkBase, generic_network_marshaller
from src.source_drivers.generic.resources.rest_schema.schema_generic_network import generic_network_all_attributes


class GenericNetworkSingular(GenericNetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_network_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_network_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, uuid):
        network = GenericNetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Generic Network not found')
        return generic_network_marshaller(network, request.args)

    @classmethod
    def put(cls, uuid):
        data = GenericNetworkSingular.parser.parse_args()
        network = GenericNetworkModel.find_by_uuid(uuid)
        if network is None:
            return generic_network_marshaller(cls.add_network(uuid, data), request.args)
        else:
            try:
                network.update(**data)
                return generic_network_marshaller(GenericNetworkModel.find_by_uuid(uuid), request.args)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def patch(cls, uuid):
        data = GenericNetworkSingular.patch_parser.parse_args()
        network = GenericNetworkModel.find_by_uuid(uuid)
        if network is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                network.update(**data)
                return generic_network_marshaller(GenericNetworkModel.find_by_uuid(uuid), request.args)
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
