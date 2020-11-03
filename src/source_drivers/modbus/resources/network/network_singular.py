from flask_restful import marshal_with, abort

from src.source_drivers.modbus.interfaces.network.network import ModbusType, ModbusRtuParity
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.network.network_base import ModbusNetworkBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_fields


class ModbusNetworkSingular(ModbusNetworkBase):

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
        data = ModbusNetworkBase.parser.parse_args()
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network is None:
            return cls.add_network(uuid, data)
        else:
            try:
                if data.type:
                    data.type = ModbusType.__members__.get(data.type)
                if data.rtu_parity:
                    data.rtu_parity = ModbusRtuParity.__members__.get(data.rtu_parity)
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
