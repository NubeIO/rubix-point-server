from flask_restful import Resource, abort
from flask_restful.reqparse import request

from src.models.network.model_network import NetworkModel
from src.resources.rest_schema.schema_network import network_all_fields, network_all_fields_with_children, \
    network_all_fields_without_point_children
from src.resources.utils import model_network_marshaller


def network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, network_all_fields,
                                    network_all_fields_without_point_children,
                                    network_all_fields_with_children)


class NetworkResource(Resource):
    @classmethod
    def get(cls, uuid):
        network = NetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Network not found')
        return network_marshaller(network, request.args)


class NetworkResourceByName(Resource):
    @classmethod
    def get(cls, name):
        network = NetworkModel.find_by_name(name)
        if not network:
            abort(404, message='Network not found')
        return network_marshaller(network, request.args)


class NetworkResourceList(Resource):
    @classmethod
    def get(cls):
        return network_marshaller(NetworkModel.query.all(), request.args)
