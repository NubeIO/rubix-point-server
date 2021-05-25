from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.network.model_network import NetworkModel
from src.resources.rest_schema.schema_network import network_all_fields, network_all_fields_with_children, \
    network_all_fields_without_point_children
from src.resources.utils import model_network_marshaller


def network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, network_all_fields,
                                    network_all_fields_without_point_children,
                                    network_all_fields_with_children)


class NetworkResourceByUUID(RubixResource):
    @classmethod
    def get(cls, uuid):
        network = NetworkModel.find_by_uuid(uuid, **request.args)
        if not network:
            raise NotFoundException('Network not found')
        return network_marshaller(network, request.args)


class NetworkResourceByName(RubixResource):
    @classmethod
    def get(cls, name):
        network = NetworkModel.find_by_name(name, **request.args)
        if not network:
            raise NotFoundException('Network not found')
        return network_marshaller(network, request.args)


class NetworkResourceList(RubixResource):
    @classmethod
    def get(cls):
        return network_marshaller(NetworkModel.find_all(**request.args), request.args)
