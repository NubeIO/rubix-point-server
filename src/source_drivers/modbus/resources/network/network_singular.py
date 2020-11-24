from flask_restful import marshal_with, abort, reqparse

from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.network.network_base import ModbusNetworkBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_fields, \
    modbus_network_all_attributes


class ModbusNetworkSingular(ModbusNetworkBase):
    patch_parser = reqparse.RequestParser()
    for attr in modbus_network_all_attributes:
        patch_parser.add_argument(attr, type=modbus_network_all_attributes[attr].get('type'), required=False)

    @classmethod
    @marshal_with(modbus_network_all_fields)
    def get(cls, uuid):
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Modbus Network not found')
        return network

    @classmethod
    @marshal_with(modbus_network_all_fields)
    def put(cls, uuid):
        data = ModbusNetworkSingular.parser.parse_args()
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network is None:
            return cls.add_network(uuid, data)
        else:
            try:
                network.update(**data)
                return ModbusNetworkModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @marshal_with(modbus_network_all_fields)
    def patch(cls, uuid):
        data = ModbusNetworkSingular.patch_parser.parse_args()
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network is None:
            abort(404, message=f"Does not exist {uuid}")
        else:
            try:
                network.update(**data)
                return ModbusNetworkModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    @classmethod
    def delete(cls, uuid):
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network:
            network.delete_from_db()
        return '', 204
