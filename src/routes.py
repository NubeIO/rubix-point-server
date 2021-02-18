from flask import Blueprint
from flask_restful import Api

from src.resources.resource_device import DeviceResource, DeviceResourceByName, DeviceResourceList
from src.resources.resource_network import NetworkResource, NetworkResourceByName, NetworkResourceList
from src.resources.resource_point import PointResource, PointResourceByName, PointResourceList
from src.resources.resource_wires_plat import WiresPlatResource
from src.source_drivers.generic.resources.device.device_plural import GenericDevicePlural
from src.source_drivers.generic.resources.device.device_singular import GenericDeviceSingular
from src.source_drivers.generic.resources.network.network_plural import GenericNetworkPlural
from src.source_drivers.generic.resources.network.network_singular import GenericNetworkSingular
from src.source_drivers.generic.resources.point.point_plural import GenericPointPlural
from src.source_drivers.generic.resources.point.point_singular import GenericPointSingular
from src.source_drivers.generic.resources.point.point_value_writer import GenericUUIDPointValueWriter, \
    GenericNamePointValueWriter
from src.source_drivers.modbus.resources.device.device_plural import ModbusDevicePlural
from src.source_drivers.modbus.resources.device.device_singular import ModbusDeviceSingular
from src.source_drivers.modbus.resources.device.device_singular_by_name import ModbusDeviceSingularByName
from src.source_drivers.modbus.resources.mapping.mapping import MPGBPMappingResourceList, \
    MPGBPMappingResourceByGenericPointUUID, MPGBPMappingResourceByBACnetPointUUID, \
    MPGBPMappingResourceByModbusPointUUID, MPGBPMappingResourceByUUID
from src.source_drivers.modbus.resources.network.network_plural import ModbusNetworkPlural
from src.source_drivers.modbus.resources.network.network_singular import ModbusNetworkSingular
from src.source_drivers.modbus.resources.network.network_singular_by_name import ModbusNetworkSingularByName
from src.source_drivers.modbus.resources.point.point_plural import ModbusPointPlural
from src.source_drivers.modbus.resources.point.point_poll import ModbusPointPollNonExisting, ModbusPointPoll
from src.source_drivers.modbus.resources.point.point_singular import ModbusPointSingular
from src.source_drivers.modbus.resources.point.point_singular_by_name import ModbusPointSingularByName
from src.source_drivers.modbus.resources.point.point_stores import ModbusPointPluralPointStore, ModbusPointStore, \
    ModbusDevicePointPluralPointStore
from src.system.resources.memory import GetSystemMem
from src.system.resources.ping import Ping

bp_network = Blueprint('networks', __name__, url_prefix='/api/networks')
api_network = Api(bp_network)
api_network.add_resource(NetworkResource, '/uuid/<string:uuid>')
api_network.add_resource(NetworkResourceByName, '/name/<string:name>')
api_network.add_resource(NetworkResourceList, '')

bp_device = Blueprint('devices', __name__, url_prefix='/api/devices')
api_network = Api(bp_device)
api_network.add_resource(DeviceResource, '/uuid/<string:uuid>')
api_network.add_resource(DeviceResourceByName, '/name/<string:network_name>/<string:device_name>')
api_network.add_resource(DeviceResourceList, '')

bp_point = Blueprint('points', __name__, url_prefix='/api/points')
api_point = Api(bp_point)
api_point.add_resource(PointResource, '/uuid/<string:uuid>')
api_point.add_resource(PointResourceByName, '/name/<string:network_name>/<string:device_name>/<string:point_name>')
api_point.add_resource(PointResourceList, '')

bp_generic = Blueprint('generic', __name__, url_prefix='/api/generic')
api_generic = Api(bp_generic)
api_generic.add_resource(GenericNetworkPlural, '/networks')
api_generic.add_resource(GenericNetworkSingular, '/networks/<string:uuid>')
api_generic.add_resource(GenericDevicePlural, '/devices')
api_generic.add_resource(GenericDeviceSingular, '/devices/<string:uuid>')
api_generic.add_resource(GenericPointPlural, '/points')
api_generic.add_resource(GenericPointSingular, '/points/<string:uuid>')
api_generic.add_resource(GenericUUIDPointValueWriter, '/points_value/uuid/<string:uuid>')
api_generic.add_resource(GenericNamePointValueWriter,
                         '/points_value/name/<string:network_name>/<string:device_name>/<string:point_name>')

bp_modbus = Blueprint('modbus', __name__, url_prefix='/api/modbus')
api_modbus = Api(bp_modbus)
api_modbus.add_resource(ModbusNetworkPlural, '/networks')
api_modbus.add_resource(ModbusNetworkSingular, '/networks/uuid/<string:uuid>')
api_modbus.add_resource(ModbusNetworkSingularByName, '/networks/name/<string:name>')
api_modbus.add_resource(ModbusDevicePlural, '/devices')
api_modbus.add_resource(ModbusDeviceSingular, '/devices/uuid/<string:uuid>')
api_modbus.add_resource(ModbusDeviceSingularByName, '/devices/name/<string:network_name>/<string:device_name>')
api_modbus.add_resource(ModbusPointPlural, '/points')
api_modbus.add_resource(ModbusPointSingular, '/points/uuid/<string:uuid>')
api_modbus.add_resource(ModbusPointSingularByName,
                        '/points/name/<string:network_name>/<string:device_name>/<string:point_name>')
api_modbus.add_resource(ModbusPointPoll, '/poll/point/<string:uuid>')
api_modbus.add_resource(ModbusPointPollNonExisting, '/poll/point')
api_modbus.add_resource(ModbusPointPluralPointStore, '/point_stores')
api_modbus.add_resource(ModbusPointStore, '/point_stores/<string:uuid>')
api_modbus.add_resource(ModbusDevicePointPluralPointStore, '/<string:device_uuid>/point_stores')

# Modbus <> Generic|BACnet points mappings
bp_mapping_mp_gbp = Blueprint('mappings_mp_gbp', __name__, url_prefix='/api/mp_gbp/mappings')
api_mapping_mp_gbp = Api(bp_mapping_mp_gbp)
api_mapping_mp_gbp.add_resource(MPGBPMappingResourceList, '')
api_mapping_mp_gbp.add_resource(MPGBPMappingResourceByUUID, '/uuid/<string:uuid>')
api_mapping_mp_gbp.add_resource(MPGBPMappingResourceByModbusPointUUID, '/modbus/<string:uuid>')
api_mapping_mp_gbp.add_resource(MPGBPMappingResourceByGenericPointUUID, '/generic/<string:uuid>')
api_mapping_mp_gbp.add_resource(MPGBPMappingResourceByBACnetPointUUID, '/bacnet/<string:uuid>')

bp_wires = Blueprint('wires', __name__, url_prefix='/api/wires')
Api(bp_wires).add_resource(WiresPlatResource, '/plat')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(Ping, '/ping')
