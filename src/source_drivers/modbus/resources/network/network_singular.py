from flask_restful import abort, reqparse
from flask_restful.reqparse import request

from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.network.network_base import ModbusNetworkBase, modbus_network_marshaller
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_attributes


class ModbusNetworkSingular(ModbusNetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in modbus_network_all_attributes:
        patch_parser.add_argument(attr,
                                  type=modbus_network_all_attributes[attr].get('type'),
                                  required=False,
                                  store_missing=False)

    @classmethod
    def get(cls, **kwargs):
        network: ModbusNetworkModel = cls.find_network(**kwargs)
        if not network:
            abort(404, message='Modbus Network not found')
        return modbus_network_marshaller(network, request.args)

    # TODO: don't allow type in patch
    @classmethod
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        network: ModbusNetworkModel = cls.find_network(**kwargs)
        if network is None:
            return modbus_network_marshaller(cls.add_network(data), request.args)
        try:
            network.update(**data)
            return modbus_network_marshaller(cls.find_network(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        network: ModbusNetworkModel = cls.find_network(**kwargs)
        if network is None:
            abort(404, message=f"Does not exist {kwargs}")
        try:
            network.update(**data)
            return modbus_network_marshaller(cls.find_network(**kwargs), request.args)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, **kwargs):
        network: ModbusNetworkModel = cls.find_network(**kwargs)
        if not network:
            abort(404, message=f"Not found {kwargs}")
        network.delete_from_db()
        return '', 204

    @classmethod
    def find_network(cls, **kwargs) -> ModbusNetworkModel:
        raise NotImplementedError


class ModbusNetworkSingularByUUID(ModbusNetworkSingular):
    @classmethod
    def find_network(cls, **kwargs) -> ModbusNetworkModel:
        return ModbusNetworkModel.find_by_uuid(kwargs.get('uuid'))


class ModbusNetworkSingularByName(ModbusNetworkSingular):
    @classmethod
    def find_network(cls, **kwargs) -> ModbusNetworkModel:
        return ModbusNetworkModel.find_by_name(kwargs.get('name'))
