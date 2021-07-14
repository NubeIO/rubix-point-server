from flask_restful.reqparse import request

from src.drivers.modbus.models.network import ModbusNetworkModel
from src.drivers.modbus.resources.network.network_base import ModbusNetworkBase, modbus_network_marshaller


class ModbusNetworkPlural(ModbusNetworkBase):
    @classmethod
    def get(cls):
        return modbus_network_marshaller(ModbusNetworkModel.find_all(), request.args)

    @classmethod
    def post(cls):
        data = ModbusNetworkPlural.parser.parse_args()
        return modbus_network_marshaller(cls.add_network(data), request.args)
