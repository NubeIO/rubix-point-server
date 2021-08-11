from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.models.network.model_network import NetworkModel
from src.resources.network.network_base import NetworkBase, network_marshaller
from src.resources.rest_schema.schema_network import network_all_attributes


class NetworkSingular(NetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in network_all_attributes:
        patch_parser.add_argument(attr,
                                  type=network_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        network: NetworkModel = cls.get_network(**kwargs)
        if not network:
            raise NotFoundException('Generic Network not found')
        return network_marshaller(network, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network: NetworkModel = cls.get_network(**kwargs)
        if network is None:
            return network_marshaller(cls.add_network(data), request.args)
        network.update(**data)
        return network_marshaller(cls.get_network(**kwargs), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network: NetworkModel = cls.get_network(**kwargs)
        if network is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network.update(**data)
        return network_marshaller(cls.get_network(**kwargs), request.args)

    @classmethod
    def delete(cls, **kwargs):
        network: NetworkModel = cls.get_network(**kwargs)
        if network is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_network(cls, **kwargs) -> NetworkModel:
        raise NotImplementedError


class NetworkSingularByUUID(NetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> NetworkModel:
        return NetworkModel.find_by_uuid(kwargs.get('uuid'))


class NetworkSingularByName(NetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> NetworkModel:
        return NetworkModel.find_by_name(kwargs.get('name'))
