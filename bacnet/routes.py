from flask_restful import Api
from bacnet import app
from bacnet.resources.device import Device, DeviceList, DevicePoints, DevicePoint
from bacnet.resources.network import Network, NetworkList, NetworksIds

from bacnet.resources.mod_network import ModNetwork, ModNetworkList, ModNetworksIds

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
api.add_resource(ModNetwork, f'/{api_ver}/modbus/network/<string:uuid>')  # CRUD a modbus network
api.add_resource(ModNetworkList, f'/{api_ver}/modbus/networks')  # get all modbus networks
