from flask_restful import Resource, reqparse
from models.device import DeviceModel


class Device(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bac_device_mac',
                        type=int,
                        required=False,
                        help='BACnet mstp device bac_device_mac address'
                        )
    parser.add_argument('bac_device_id',
                        type=int,
                        required=True,
                        help='Every device needs a bacnet device id'
                        )
    parser.add_argument('bac_device_ip',
                        type=str,
                        required=True,
                        help='Every device needs a network bac_device_ip.'
                        )
    parser.add_argument('bac_device_mask',
                        type=int,
                        required=True,
                        help='Every device needs a network bac_device_mask.'
                        )
    parser.add_argument('bac_device_port',
                        type=int,
                        required=True,
                        help='Every device needs a network bac_device_port.'
                        )
    parser.add_argument('network_uuid',
                        type=str,
                        required=True,
                        help='Every device needs a network bac_device_uuid.'
                        )

    # bac_device_mac, bac_device_id , bac_device_ip, bac_device_mask, bac_device_port, network_id
    # @jwt_required()
    def get(self, name):
        bac_device_uuid = name
        device = DeviceModel.find_by_bac_device_uuid(bac_device_uuid)
        if device:
            return device.get_device()
        return {'message': 'device not found.'}, 404

    def post(self, name):
        bac_device_uuid = name
        if DeviceModel.find_by_bac_device_uuid(bac_device_uuid):
            return {'message': "An device with bac_device_uuid '{}' already exists.".format(bac_device_uuid)}, 400

        data = Device.parser.parse_args()

        device = DeviceModel(bac_device_uuid, data['bac_device_mac'], data['bac_device_id'], data['bac_device_ip'],
                             data['bac_device_mask'], data['bac_device_port'],
                             data['network_uuid'])
        try:
            device.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the device.'}, 500
        return device.get_device(), 201

    def delete(self, name):
        bac_device_uuid = name
        device = DeviceModel.find_by_bac_device_uuid(bac_device_uuid)
        if device:
            device.delete_from_db()
        return {'message': 'device deleted'}

    def patch(self, name):
        bac_device_uuid = name
        data = Device.parser.parse_args()
        print(data)

        device = DeviceModel.find_by_bac_device_uuid(bac_device_uuid)

        if device is None:
            device = DeviceModel(bac_device_uuid, data['bac_device_mac'], data['bac_device_id'], data['bac_device_ip'],
                                 data['bac_device_mask'], data['bac_device_port'],
                                 data['network_uuid'])
        else:
            device.bac_device_mac = data['bac_device_mac']
            device.bac_device_id = data['bac_device_id']
            device.bac_device_ip = data['bac_device_ip']
            device.bac_device_mask = data['bac_device_mask']
            device.bac_device_port = data['bac_device_port']
            device.network_id = data['network_uuid']

        device.save_to_db()

        return device.get_device()


class DeviceList(Resource):

    def get(self):
        return {'devices': [device.get_device() for device in DeviceModel.query.all()]}
