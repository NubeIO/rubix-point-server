from flask_restful import Api
from bacnet import app
from bacnet.resources.device import Device, DeviceList, DevicePoints
from bacnet.resources.network import Network, NetworkList, NetworksIds

api_ver = 'api/1.1'
api = Api(app)

api.add_resource(Device, f'/{api_ver}/device/<string:uuid>')
api.add_resource(Network, f'/{api_ver}/network/<string:uuid>')
api.add_resource(DeviceList, f'/{api_ver}/devices')  # get all devices
api.add_resource(DevicePoints, f'/{api_ver}/device/points/obj/<string:dev_uuid>')  # get all networks DevicePoints
api.add_resource(NetworkList, f'/{api_ver}/networks')  # get all networks
api.add_resource(NetworksIds, f'/{api_ver}/networks/ids')  # get all networks DevicePoints
