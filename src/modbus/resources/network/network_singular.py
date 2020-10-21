from flask_restful import marshal_with, abort

from src.modbus.interfaces.network.network import ModbusType, ModbusRtuParity
from src.modbus.models.network import ModbusNetworkModel
from src.modbus.resources.mod_fields import network_fields
from src.modbus.resources.network.network_plural import ModusNetworkPlural
from src.modbus.resources.network.network_base import ModusNetworkBase


class ModusNetworkSingular(ModusNetworkBase):

    @marshal_with(network_fields)
    def get(self, uuid):
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if not network:
            abort(404, message='Modbus Network not found')
        return network

    @marshal_with(network_fields)
    def put(self, uuid):
        data = ModusNetworkPlural.parser.parse_args()
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network is None:
            return self.add_network(uuid, data)
        else:
            try:
                if data.type:
                    data.type = ModbusType.__members__.get(data.type)
                if data.rtu_parity:
                    data.rtu_parity = ModbusRtuParity.__members__.get(data.rtu_parity)
                ModbusNetworkModel.filter_by_uuid(uuid).update(data)
                ModbusNetworkModel.commit()
                return ModbusNetworkModel.find_by_uuid(uuid)
            except Exception as e:
                abort(500, message=str(e))

    def delete(self, uuid):
        network = ModbusNetworkModel.find_by_uuid(uuid)
        if network:
            network.delete_from_db()
        return '', 204
