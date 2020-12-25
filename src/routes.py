from flask import Blueprint
from flask_restful import Api

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

bp_network = Blueprint('networks', __name__, url_prefix='/api/networks')
api_network = Api(bp_network)
api_network.add_resource(NetworkResource, '/uuid/<string:uuid>')
api_network.add_resource(NetworkResourceByName, '/name/<string:name>')
api_network.add_resource(NetworkResourceList, '/')

bp_device = Blueprint('devices', __name__, url_prefix='/api/devices')
api_network = Api(bp_device)
api_network.add_resource(DeviceResource, '/uuid/<string:uuid>')
api_network.add_resource(DeviceResourceByName, '/name/<string:network_name>/<string:device_name>')
api_network.add_resource(DeviceResourceList, '/')

bp_point = Blueprint('points', __name__, url_prefix='/api/points')
api_point = Api(bp_point)
api_point.add_resource(PointResource, '/uuid/<string:uuid>')
api_point.add_resource(PointResourceByName, '/name/<string:network_name>/<string:device_name>/<string:point_name>')
api_point.add_resource(PointResourceList, '/')

# common parent inheritance endpoints
# api.add_resource(PointReadOnlyResourceList, '/readonly')
# api.add_resource(PointWriteableResourceList, '/writable')

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

bp_generic = Blueprint('generic', __name__, url_prefix='/api/generic')
api_generic = Api(bp_generic)
api_generic.add_resource(GenericNetworkPlural, '/networks')
api_generic.add_resource(GenericNetworkSingular, '/networks/<string:uuid>')
api_generic.add_resource(GenericDevicePlural, '/devices')
api_generic.add_resource(GenericDeviceSingular, '/devices/<string:uuid>')
api_generic.add_resource(GenericPointPlural, '/points')
api_generic.add_resource(GenericPointSingular, '/points/<string:uuid>')

bp_modbus = Blueprint('modbus', __name__, url_prefix='/api/modbus')
api_modbus = Api(bp_modbus)
api_modbus.add_resource(ModbusNetworkPlural, '/networks')
api_modbus.add_resource(ModbusNetworkSingular, '/networks/<string:uuid>')
api_modbus.add_resource(ModbusDevicePlural, '/devices')
api_modbus.add_resource(ModbusDeviceSingular, '/devices/<string:uuid>')
api_modbus.add_resource(ModbusPointPlural, '/points')
api_modbus.add_resource(ModbusPointSingular, '/points/<string:uuid>')
api_modbus.add_resource(ModbusPointPoll, '/poll/point/<string:uuid>')
api_modbus.add_resource(ModbusPointPollNonExisting, '/poll/point')
api_modbus.add_resource(ModbusPointPluralPointStore, '/point_stores')
api_modbus.add_resource(ModbusPointStore, '/point_stores/<string:uuid>')
api_modbus.add_resource(ModbusDevicePointPluralPointStore, '/<string:device_uuid>/point_stores')

bp_wires = Blueprint('wires', __name__, url_prefix='/api/wires')
Api(bp_wires).add_resource(WiresPlatResource, '/plat')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(Ping, '/', '/ping')
