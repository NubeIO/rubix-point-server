from flask_restful import Resource, reqparse, marshal_with, abort

from src.models.network.model_network import NetworkModel
from src.resources.rest_schema.schema_network import network_all_attributes, network_all_fields


class NetworkResource(Resource):
    parser = reqparse.RequestParser()
    for attr in network_all_attributes:
        parser.add_argument(attr,
                            type=network_all_attributes[attr].get('type'),
                            required=network_all_attributes[attr].get('required', False),
                            help=network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(network_all_fields)
    def get(cls, uuid):
        network = NetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Network not found')
        return network


class NetworkResourceByName(Resource):
    @classmethod
    @marshal_with(network_all_fields)
    def get(cls, name):
        network = NetworkModel.find_by_name(name)
        if not network:
            abort(404, message='Network not found')
        return network


class NetworkResourceList(Resource):
    @classmethod
    @marshal_with(network_all_fields)
    def get(cls):
        return NetworkModel.query.all()
