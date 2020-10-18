from flask_restful import Api
from src import app
from src.resources.bacnet.device import Device, DeviceList, DevicePoints, DevicePoint
from src.resources.bacnet.network import Network, NetworkList, NetworksIds

from src.resources.modbus.mod_network import ModNetwork, ModNetworkList
from src.resources.modbus.mod_device import ModDevice, ModDeviceList
from src.resources.modbus.mod_point import ModPoint, ModPointList

api_ver = 'api'
api = Api(app)

# bacnet endpoints
api.add_resource(Device, f'/{api_ver}/bacnet/dev/<string:uuid>')
api.add_resource(Network, f'/{api_ver}/bacnet/network/<string:uuid>')
api.add_resource(DeviceList, f'/{api_ver}/bacnet/devices')  # get all devices
api.add_resource(DevicePoints, f'/{api_ver}/bacnet/points/objects/<string:dev_uuid>')  # get all networks DevicePoints
api.add_resource(DevicePoint, f'/{api_ver}/bacnet/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')  # get a point /dev_uuid/analogInput/1
api.add_resource(NetworkList, f'/{api_ver}/bacnet/networks')  # get all networks
api.add_resource(NetworksIds, f'/{api_ver}/bacnet/networks/ids')  # get all networks DevicePoints

# modbus endpoints

# networks
api.add_resource(ModNetwork, f'/{api_ver}/modbus/network/<string:uuid>')  # CRUD a modbus network
api.add_resource(ModNetworkList, f'/{api_ver}/modbus/networks')  # get all modbus networks
# devices
api.add_resource(ModDevice, f'/{api_ver}/modbus/device/<string:uuid>')  # CRUD a modbus device
api.add_resource(ModDeviceList, f'/{api_ver}/modbus/devices')  # get all modbus devices
# points
api.add_resource(ModPoint, f'/{api_ver}/modbus/point/<string:uuid>')  # CRUD a modbus device
api.add_resource(ModPointList, f'/{api_ver}/modbus/points')  # get all modbus devices

