from flask_restful import Api

from src import app
from src.resources.resource_device import DeviceResource, DeviceResourceByName, DeviceResourceList
from src.resources.resource_network import NetworkResource, NetworkResourceByName, NetworkResourceList
from src.resources.resource_point import PointResource, PointResourceByName, PointResourceList
from src.resources.resource_wires_plat import WiresPlatResource
# from src.source_drivers.bacnet.resources.device import Device, DeviceList, DevicePoints, DevicePoint
# from src.source_drivers.bacnet.resources.network import Network, NetworkList, NetworksIds
from src.source_drivers.generic.resources.device.device_plural import GenericDevicePlural
from src.source_drivers.generic.resources.device.device_singular import GenericDeviceSingular
from src.source_drivers.generic.resources.network.network_plural import GenericNetworkPlural
from src.source_drivers.generic.resources.network.network_singular import GenericNetworkSingular
from src.source_drivers.generic.resources.point.point_plural import GenericPointPlural
from src.source_drivers.generic.resources.point.point_singular import GenericPointSingular

from src.source_drivers.modbus.resources.device.device_plural import ModbusDevicePlural
from src.source_drivers.modbus.resources.device.device_singular import ModbusDeviceSingular
from src.source_drivers.modbus.resources.network.network_plural import ModbusNetworkPlural
from src.source_drivers.modbus.resources.network.network_singular import ModbusNetworkSingular
from src.source_drivers.modbus.resources.point.point_plural import ModbusPointPlural
from src.source_drivers.modbus.resources.point.point_singular import ModbusPointSingular, ModbusPointPoll, \
    ModbusPointPollNonExisting
from src.source_drivers.modbus.resources.point.point_stores import ModbusPointPluralPointStore, ModbusPointStore, \
    ModbusDevicePointPluralPointStore
from src.system.resources.memory import GetSystemMem
from src.system.resources.ping import Ping

api_prefix = 'api'
api = Api(app)

# common parent inheritance endpoints
api.add_resource(NetworkResource, f'/{api_prefix}/networks/uuid/<string:uuid>')
api.add_resource(NetworkResourceByName, f'/{api_prefix}/networks/name/<string:name>')
api.add_resource(NetworkResourceList, f'/{api_prefix}/networks')
api.add_resource(DeviceResource, f'/{api_prefix}/devices/uuid/<string:uuid>')
api.add_resource(DeviceResourceByName, f'/{api_prefix}/devices/name/<string:network_name>/<string:device_name>')
api.add_resource(DeviceResourceList, f'/{api_prefix}/devices')
api.add_resource(PointResource, f'/{api_prefix}/points/uuid/<string:uuid>')
api.add_resource(PointResourceByName, f'/{api_prefix}/points/name/<string:network_name>/<string:device_name>/'
                                      f'<string:point_name>')
api.add_resource(PointResourceList, f'/{api_prefix}/points')
# api.add_resource(PointReadOnlyResourceList, f'/{api_prefix}/points/readonly')
# api.add_resource(PointWriteableResourceList, f'/{api_prefix}/points/writable')

# bacnet_api_prefix = f'{api_prefix}/bacnet'
# api.add_resource(Device, f'/{bacnet_api_prefix}/dev/<string:uuid>')
# api.add_resource(Network, f'/{bacnet_api_prefix}/network/<string:uuid>')
# api.add_resource(DeviceList, f'/{bacnet_api_prefix}/devices')
# api.add_resource(DevicePoints, f'/{bacnet_api_prefix}/points/objects/<string:dev_uuid>')
# # get a point /dev_uuid/analogInput/1
# api.add_resource(DevicePoint,
#                  f'/{bacnet_api_prefix}/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')
# api.add_resource(NetworkList, f'/{bacnet_api_prefix}/networks')
# api.add_resource(NetworksIds, f'/{bacnet_api_prefix}/networks/ids')

generic_api_prefix = f'{api_prefix}/generic'
api.add_resource(GenericNetworkPlural, f'/{generic_api_prefix}/networks')
api.add_resource(GenericNetworkSingular, f'/{generic_api_prefix}/networks/<string:uuid>')
api.add_resource(GenericDevicePlural, f'/{generic_api_prefix}/devices')
api.add_resource(GenericDeviceSingular, f'/{generic_api_prefix}/devices/<string:uuid>')
api.add_resource(GenericPointPlural, f'/{generic_api_prefix}/points')
api.add_resource(GenericPointSingular, f'/{generic_api_prefix}/points/<string:uuid>')

modbus_api_prefix = f'{api_prefix}/modbus'
api.add_resource(ModbusNetworkPlural, f'/{modbus_api_prefix}/networks')
api.add_resource(ModbusNetworkSingular, f'/{modbus_api_prefix}/networks/<string:uuid>')
api.add_resource(ModbusDevicePlural, f'/{modbus_api_prefix}/devices')
api.add_resource(ModbusDeviceSingular, f'/{modbus_api_prefix}/devices/<string:uuid>')
api.add_resource(ModbusPointPlural, f'/{modbus_api_prefix}/points')
api.add_resource(ModbusPointSingular, f'/{modbus_api_prefix}/points/<string:uuid>')
api.add_resource(ModbusPointPoll, f'/{modbus_api_prefix}/poll/point/<string:uuid>')
api.add_resource(ModbusPointPollNonExisting, f'/{modbus_api_prefix}/poll/point')
api.add_resource(ModbusPointPluralPointStore, f'/{modbus_api_prefix}/point_stores')
api.add_resource(ModbusPointStore, f'/{modbus_api_prefix}/point_stores/<string:uuid>')
api.add_resource(ModbusDevicePointPluralPointStore, f'/{modbus_api_prefix}/<string:device_uuid>/point_stores')

wires_api_prefix = f'{api_prefix}/wires'
api.add_resource(WiresPlatResource, f'/{wires_api_prefix}/plat')

system_api_prefix = f'{api_prefix}/system'
api.add_resource(GetSystemMem, f'/{system_api_prefix}/memory')
api.add_resource(Ping, f'/{system_api_prefix}', f'/{system_api_prefix}/ping')
