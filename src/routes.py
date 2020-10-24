from flask_restful import Api

from src import app
from src.bacnet.resources.device import Device, DeviceList, DevicePoints, DevicePoint
from src.bacnet.resources.network import Network, NetworkList, NetworksIds
from src.modbus.resources.device.device_plural import ModbusDevicePlural
from src.modbus.resources.device.device_singular import ModbusDeviceSingular
from src.modbus.resources.network.network_plural import ModusNetworkPlural
from src.modbus.resources.network.network_singular import ModusNetworkSingular
from src.modbus.resources.point.point_plural import ModbusPointPlural, ModbusPointPluralPointStore
from src.modbus.resources.point.point_singular import ModbusPointSingular

api_prefix = 'api'
api = Api(app)

# bacnet endpoints
api.add_resource(Device, f'/{api_prefix}/bacnet/dev/<string:uuid>')
api.add_resource(Network, f'/{api_prefix}/bacnet/network/<string:uuid>')
api.add_resource(DeviceList, f'/{api_prefix}/bacnet/devices')  # get all devices
api.add_resource(DevicePoints,
                 f'/{api_prefix}/bacnet/points/objects/<string:dev_uuid>')  # get all networks DevicePoints
# get a point /dev_uuid/analogInput/1
api.add_resource(DevicePoint,
                 f'/{api_prefix}/bacnet/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')
api.add_resource(NetworkList, f'/{api_prefix}/bacnet/networks')  # get all networks
api.add_resource(NetworksIds, f'/{api_prefix}/bacnet/networks/ids')  # get all networks DevicePoints

# Modbus endpoints --------------------------------------
api.add_resource(ModusNetworkPlural, f'/{api_prefix}/modbus/networks')
api.add_resource(ModusNetworkSingular, f'/{api_prefix}/modbus/networks/<string:uuid>')

api.add_resource(ModbusDevicePlural, f'/{api_prefix}/modbus/devices')
api.add_resource(ModbusDeviceSingular, f'/{api_prefix}/modbus/devices/<string:uuid>')

api.add_resource(ModbusPointPlural, f'/{api_prefix}/modbus/points')
api.add_resource(ModbusPointPluralPointStore, f'/{api_prefix}/modbus/<string:device_uuid>/points_store')
api.add_resource(ModbusPointSingular, f'/{api_prefix}/modbus/points/<string:uuid>')
