from abc import abstractmethod

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
    def get(cls, **kwargs):
        network: GenericNetworkModel = cls.get_network(**kwargs)
        if not network:
            abort(404, message='Generic Network not found')
        return generic_network_marshaller(network, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network: GenericNetworkModel = cls.get_network(**kwargs)
        if network is None:
            return generic_network_marshaller(cls.add_network(data), request.args)
        try:
            network.update(**data)
            return generic_network_marshaller(cls.get_network(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network: GenericNetworkModel = cls.get_network(**kwargs)
        if network is None:
            abort(404, message=f"Does not exist {kwargs}")
        try:
            network.update(**data)
            return generic_network_marshaller(cls.get_network(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        network: GenericNetworkModel = cls.get_network(**kwargs)
        if network is None:
            abort(404, message=f"Does not exist {kwargs}")
        network.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_network(cls, **kwargs) -> GenericNetworkModel:
        raise NotImplementedError


class GenericNetworkSingularByUUID(GenericNetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> GenericNetworkModel:
        return GenericNetworkModel.find_by_uuid(kwargs.get('uuid'))


class GenericNetworkSingularByName(GenericNetworkSingular):
    @classmethod
    def get_network(cls, **kwargs) -> GenericNetworkModel:
        return GenericNetworkModel.find_by_name(kwargs.get('name'))
