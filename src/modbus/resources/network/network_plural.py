import uuid
from flask_restful import marshal_with

from src.modbus.models.network import ModbusNetworkModel
from src.modbus.resources.mod_fields import network_fields
from src.modbus.resources.network.network_base import ModusNetworkBase


class ModusNetworkPlural(ModusNetworkBase):
    @marshal_with(network_fields, envelope="networks")
    def get(self):
        return ModbusNetworkModel.query.all()

    @marshal_with(network_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = ModusNetworkPlural.parser.parse_args()
        return self.add_network(_uuid, data)
