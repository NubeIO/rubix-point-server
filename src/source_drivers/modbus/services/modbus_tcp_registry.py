import logging

from pymodbus.client.sync import ModbusTcpClient

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.services.modbus_registry import ModbusRegistryKey, ModbusRegistry, \
    ModbusRegistryConnection

logger = logging.getLogger(__name__)


class ModbusTcpRegistryKey(ModbusRegistryKey):
    def create_connection_key(self) -> str:
        return f'{self.device.tcp_ip}:{self.device.tcp_port}:{self.device.timeout}'


class ModbusTcpRegistry(ModbusRegistry):

    def add_connection(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusRegistryConnection:
        host: str = device.tcp_ip
        port: int = device.tcp_port
        timeout: int = device.timeout
        registry_key: ModbusTcpRegistryKey = ModbusTcpRegistryKey(network, device)
        self.remove_connection_if_exist(registry_key.key)
        logger.debug(f'Adding tcp_connection {registry_key.key}')
        self.connections[registry_key.key] = ModbusRegistryConnection(
            registry_key.connection_key,
            ModbusTcpClient(host=host, port=port, timeout=timeout)
        )
        return self.connections[registry_key.key]

    def get_registry_key(self, network: ModbusNetworkModel, device: ModbusDeviceModel) -> ModbusRegistryKey:
        return ModbusTcpRegistryKey(network, device)

    def get_type(self) -> ModbusType:
        return ModbusType.TCP
