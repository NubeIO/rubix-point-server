from flask_restful import Api
from src import app


from src.resources.resource_network import NetworkResource, NetworkResourceList
from src.resources.resource_device import DeviceResource, DeviceResourceList
from src.resources.resource_point import PointResource, PointResourceList

# from src.sourceDrivers.bacnet.resources.device import Device, DeviceList, DevicePoints, DevicePoint
# from src.sourceDrivers.bacnet.resources.network import Network, NetworkList, NetworksIds

from src.sourceDrivers.modbusCopy.resources.mod_network import ModNetwork, ModNetworkList
from src.sourceDrivers.modbusCopy.resources.mod_device import ModDevice, ModDeviceList
from src.sourceDrivers.modbusCopy.resources.mod_point import ModPoint, ModPointList

api_ver = 'api'
api = Api(app)

# networks
api.add_resource(NetworkResource, f'/{api_ver}/network/<string:uuid>')  # get network
api.add_resource(NetworkResourceList, f'/{api_ver}/networks')  # get all networks
# devices
api.add_resource(DeviceResource, f'/{api_ver}/device/<string:uuid>')  # get device
api.add_resource(DeviceResourceList, f'/{api_ver}/devices')  # get all devices
# points
api.add_resource(PointResource, f'/{api_ver}/point/<string:uuid>')  # get point
api.add_resource(PointResourceList, f'/{api_ver}/points')  # get all points


# bacnet endpoints
# api.add_resource(Device, f'/{api_ver}/bacnet/dev/<string:uuid>')
# api.add_resource(Network, f'/{api_ver}/bacnet/network/<string:uuid>')
# api.add_resource(DeviceList, f'/{api_ver}/bacnet/devices')  # get all devices
# api.add_resource(DevicePoints, f'/{api_ver}/bacnet/points/objects/<string:dev_uuid>')  # get all networks DevicePoints
# api.add_resource(DevicePoint,
#                  f'/{api_ver}/bacnet/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')  # get a point /dev_uuid/analogInput/1
# api.add_resource(NetworkList, f'/{api_ver}/bacnet/networks')  # get all networks
# api.add_resource(NetworksIds, f'/{api_ver}/bacnet/networks/ids')  # get all networks DevicePoints

# modbus endpoints

# networks
api.add_resource(ModNetwork, f'/{api_ver}/modbus/network/<string:uuid>')  # CRUD a modbus network
api.add_resource(ModNetworkList, f'/{api_ver}/modbus/networks')  # get all modbus networks
# devices
api.add_resource(ModDevice, f'/{api_ver}/modbus/device/<string:uuid>')  # CRUD a modbus device
api.add_resource(ModDeviceList, f'/{api_ver}/modbus/devices')  # get all modbus devices
# points
api.add_resource(ModPoint, f'/{api_ver}/modbus/point/<string:uuid>')  # CRUD a modbus point
api.add_resource(ModPointList, f'/{api_ver}/modbus/points')  # get all modbus points
