from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.network.network_singular_base import ModbusNetworkSingularBase


class ModbusNetworkSingularByName(ModbusNetworkSingularBase):

    @classmethod
    def find_network(cls, **kwargs) -> ModbusNetworkModel:
        return ModbusNetworkModel.find_by_name(kwargs.get('name'))
