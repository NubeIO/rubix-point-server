import os
from flask import Flask
from flask_restful import Api
from resources.device import Device, DeviceList, DevicePoints
from resources.network import Network, NetworkList, NetworksIds

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

api = Api(app)

api_ver = 'api/1.1'
ip = '0.0.0.0'
port = 5000
debug = True


api.add_resource(Device, f'/{api_ver}/device/<string:uuid>')
api.add_resource(Network, f'/{api_ver}/network/<string:uuid>')
api.add_resource(DeviceList, f'/{api_ver}/devices')  # get all devices
api.add_resource(DevicePoints, f'/{api_ver}/device/points/obj/<string:dev_uuid>,<string:net_uuid>')  # get all networks DevicePoints
api.add_resource(NetworkList, f'/{api_ver}/networks')  # get all networks
api.add_resource(NetworksIds, f'/{api_ver}/networks/ids')  # get all networks DevicePoints

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host=ip, port=port, debug=debug)

