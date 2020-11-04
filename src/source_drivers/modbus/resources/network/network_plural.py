import uuid
from flask_restful import marshal_with

from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.network.network_base import ModbusNetworkBase
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_fields


class ModbusNetworkPlural(ModbusNetworkBase):
    @classmethod
    @marshal_with(modbus_network_all_fields, envelope="networks")
    def get(cls):
        return ModbusNetworkModel.query.all()

    @classmethod
    @marshal_with(modbus_network_all_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = ModbusNetworkPlural.parser.parse_args()
        return cls.add_network(_uuid, data)
