from flask_restful import Api
from bacnet import app
from bacnet.resources.device import Device, DeviceList, DevicePoints, DevicePoint
from bacnet.resources.network import Network, NetworkList, NetworksIds

api_ver = 'api'
api = Api(app)

# bacnet endpoints
api.add_resource(Device, f'/{api_ver}/bacnet/device/<string:uuid>')
api.add_resource(Network, f'/{api_ver}/bacnet/network/<string:uuid>')
api.add_resource(DeviceList, f'/{api_ver}/bacnet/devices')  # get all devices
api.add_resource(DevicePoints, f'/{api_ver}/bacnet/device/points/all/<string:dev_uuid>')  # get all networks DevicePoints
api.add_resource(DevicePoints, f'/{api_ver}/bacnet/device/objects/<string:dev_uuid>')  # get all networks DevicePoints
api.add_resource(DevicePoint, f'/{api_ver}/bacnet/device/point/read/<string:dev_uuid>/<string:obj>/<string:obj_instance>/<string:prop>')  # get a point /dev_uuid/analogInput/1
api.add_resource(NetworkList, f'/{api_ver}/bacnet/networks')  # get all networks
api.add_resource(NetworksIds, f'/{api_ver}/bacnet/networks/ids')  # get all networks DevicePoints


# modbus endpoints
api.add_resource(NetworksIds, f'/{api_ver}/bacnet/networks/ids')  # get all networks DevicePoints
api.add_resource(NetworksIds, f'/{api_ver}/modbus/networks/ids')  # get all networks DevicePoints
# future
# api.add_resource(NetworkList, f'/{api_ver}/server/networks')  # get BACnet-server all networks


# add network
# add device, on adding a device this will poll the network
# on api call / (store all points in device.points)
