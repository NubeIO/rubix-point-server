import logging

from pymodbus.client.sync import ModbusTcpClient

from src.drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.drivers.modbus.services.modbus_registry import ModbusRegistryKey, ModbusRegistry, \
    ModbusRegistryConnection

logger = logging.getLogger(__name__)


class ModbusTcpRegistryKey(ModbusRegistryKey):
    def create_connection_key(self) -> str:
        return f'{self.network.tcp_ip}:{self.network.tcp_port}:{self.network.timeout}'


class ModbusTcpRegistry(ModbusRegistry):

    def add_connection(self, network: ModbusNetworkModel) -> ModbusRegistryConnection:
        host: str = network.tcp_ip
        port: int = network.tcp_port
        timeout: int = network.timeout
        registry_key: ModbusTcpRegistryKey = ModbusTcpRegistryKey(network)
        self.remove_connection_if_exist(registry_key.key)
        logger.debug(f'Adding tcp_connection {registry_key.key}')
        self.connections[registry_key.key] = ModbusRegistryConnection(
            registry_key.connection_key,
            ModbusTcpClient(host=host, port=port, timeout=timeout)
        )
        return self.connections[registry_key.key]

    def get_registry_key(self, network: ModbusNetworkModel) -> ModbusRegistryKey:
        return ModbusTcpRegistryKey(network)

    def get_type(self) -> ModbusType:
        return ModbusType.TCP
