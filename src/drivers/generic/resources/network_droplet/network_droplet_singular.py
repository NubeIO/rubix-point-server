from abc import abstractmethod

from flask_restful import reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException

from src.drivers.generic.models.network_droplet import GenericNetworkDropletModel
from src.drivers.generic.resources.network.network_base import generic_network_marshaller
from src.drivers.generic.resources.network_droplet.network_droplet_base import GenericNetworkDropletBase, \
    generic_network_droplet_marshaller
from src.drivers.generic.resources.rest_schema.schema_generic_network_drroplet import \
    generic_network_droplet_all_attributes


class GenericNetworkDropletSingular(GenericNetworkDropletBase):
    patch_parser = reqparse.RequestParser()
    for attr in generic_network_droplet_all_attributes:
        patch_parser.add_argument(attr,
                                  type=generic_network_droplet_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        network_droplet: GenericNetworkDropletModel = cls.get_network_droplet(**kwargs)
        if not network_droplet:
            raise NotFoundException('Generic Network not found')
        return generic_network_droplet_marshaller(network_droplet, request.args)

    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network_droplet: GenericNetworkDropletModel = cls.get_network_droplet(**kwargs)
        if network_droplet is None:
            return generic_network_marshaller(cls.add_network_droplet(data), request.args)
        network_droplet.update(**data)
        return generic_network_marshaller(cls.get_network_droplet(**kwargs), request.args)

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network_droplet: GenericNetworkDropletModel = cls.get_network(**kwargs)
        if network_droplet is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network_droplet.update(**data)
        return generic_network_marshaller(cls.get_network_droplet(**kwargs), request.args)

    @classmethod
    def delete(cls, **kwargs):
        network_droplet: GenericNetworkDropletModel = cls.get_network_droplet(**kwargs)
        if network_droplet is None:
            raise NotFoundException(f"Does not exist {kwargs}")
        network_droplet.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_network_droplet(cls, **kwargs) -> GenericNetworkDropletModel:
        raise NotImplementedError


class GenericNetworkDropletSingularByUUID(GenericNetworkDropletSingular):
    @classmethod
    def get_network_droplet(cls, **kwargs) -> GenericNetworkDropletModel:
        return GenericNetworkDropletModel.find_by_uuid(kwargs.get('uuid'))


class GenericNetworkDropletSingularByName(GenericNetworkDropletSingular):
    @classmethod
    def get_network_droplet(cls, **kwargs) -> GenericNetworkDropletModel:
        return GenericNetworkDropletModel.find_by_name(kwargs.get('name'))
