from flask_restful import Resource, reqparse
from models.device import DeviceModel


class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mac',
                        type=int,
                        required=False,
                        help='BACnet mstp device mac address'
                        )
    parser.add_argument('bac_device_id',
                        type=int,
                        required=True,
                        help='Every device needs a bacnet device id'
                        )
    parser.add_argument('ip',
                        type=str,
                        required=True,
                        help='Every device needs a network ip.'
                        )
    parser.add_argument('mask',
                        type=int,
                        required=True,
                        help='Every device needs a network mask.'
                        )
    parser.add_argument('port',
                        type=int,
                        required=True,
                        help='Every device needs a network port.'
                        )
    parser.add_argument('network_uuid',
                        type=str,
                        required=True,
                        help='Every device needs a network uuid.'
                        )

    # mac, bac_device_id , ip, mask, port, network_id
    # @jwt_required()
    def get(self, name):
        uuid = name
        device = DeviceModel.find_by_uuid(uuid)
        if device:
            return device.get_device()
        return {'message': 'device not found.'}, 404

    def post(self, name):
        uuid = name
        if DeviceModel.find_by_uuid(uuid):
            return {'message': "An device with uuid '{}' already exists.".format(uuid)}, 400

        data = Device.parser.parse_args()

        device = DeviceModel(uuid, data['mac'], data['bac_device_id'], data['ip'], data['mask'], data['port'],
                             data['network_uuid'])
        try:
            device.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the device.'}, 500
        return device.get_device(), 201

    def delete(self, name):
        uuid = name
        device = DeviceModel.find_by_uuid(uuid)
        if device:
            device.delete_from_db()
        return {'message': 'device deleted'}

    def patch(self, name):
        uuid = name
        data = Device.parser.parse_args()
        print(data)

        device = DeviceModel.find_by_uuid(uuid)

        if device is None:
            device = DeviceModel(uuid, data['mac'], data['bac_device_id'], data['ip'], data['mask'], data['port'],
                                 data['network_uuid'])
        else:
            device.mac = data['mac']
            device.mac = data['bac_device_id']
            device.mac = data['ip']
            device.mac = data['mask']
            device.mac = data['port']
            device.network_id = data['network_uuid']

        device.save_to_db()

        return device.get_device()


class DeviceList(Resource):

    def get(self):
        return {'devices': [device.get_device() for device in DeviceModel.query.all()]}
