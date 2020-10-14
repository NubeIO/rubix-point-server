from flask_restful import Resource, reqparse, abort, fields, marshal_with
from bacnet.models.device import DeviceModel
from bacnet.resources.network import network_fields

device_fields = {
    'bac_device_uuid': fields.String,
    'bac_device_mac': fields.Integer,
    'bac_device_id': fields.Integer,
    'bac_device_ip': fields.String,
    'bac_device_mask': fields.Integer,
    'bac_device_port': fields.Integer,
    'network_uuid': fields.String,
}


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
                        help='Every device needs a network bac_device_mask'
                        )
    parser.add_argument('bac_device_port',
                        type=int,
                        required=True,
                        help='Every device needs a network bac_device_port'
                        )
    parser.add_argument('network_uuid',
                        type=str,
                        required=True,
                        help='Every device needs a network bac_device_uuid'
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = DeviceModel.find_by_bac_device_uuid(uuid)
        if not device:
            abort(404, message='Device not found.')
        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if DeviceModel.find_by_bac_device_uuid(uuid):
            return {'message': "An device with bac_device_uuid '{}' already exists.".format(uuid)}, 400
        data = Device.parser.parse_args()
        device = Device.create_device_model_obj(uuid, data)
        if device.find_by_bac_device_uuid(uuid) is not None:
            abort(409, message="Already exist this value")
        device.save_to_db()
        return device, 201

    @marshal_with(device_fields)
    def put(self, uuid):
        data = Device.parser.parse_args()
        device = DeviceModel.find_by_bac_device_uuid(uuid)
        if device is None:
            device = Device.create_device_model_obj(uuid, data)
        else:
            device.bac_device_mac = data['bac_device_mac']
            device.bac_device_id = data['bac_device_id']
            device.bac_device_ip = data['bac_device_ip']
            device.bac_device_mask = data['bac_device_mask']
            device.bac_device_port = data['bac_device_port']
            device.network_id = data['network_uuid']
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = DeviceModel.find_by_bac_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(bac_device_uuid, data):
        return DeviceModel(bac_device_uuid=bac_device_uuid, bac_device_mac=data['bac_device_mac'],
                           bac_device_id=data['bac_device_id'], bac_device_ip=data['bac_device_ip'],
                           bac_device_mask=data['bac_device_mask'], bac_device_port=data['bac_device_port'],
                           network_uuid=data['network_uuid'])


class DeviceList(Resource):
    @marshal_with(device_fields, envelope="devices")
    def get(self):
        return DeviceModel.query.all()


device_point_fields = network_fields
updated_device_fields = device_fields.copy()
updated_device_fields.update({'hello': fields.String})
device_point_fields['devices'] = fields.List(fields.Nested(updated_device_fields))


class DevicePoints(Resource):
    def get(self, dev_uuid):
        response = {}
        device = DeviceModel.find_by_bac_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['bac_device_uuid'] = device.bac_device_uuid
        response['bac_device_mac'] = device.bac_device_mac
        from bacnet.services.device import Device as DeviceService
        response['points'] = DeviceService.get_instance().get_points(device)
        return response

class DevicePoint(Resource):
    def get(self, dev_uuid, obj, obj_instance, prop):
        # def get(self, dev_uuid, pnt_type, pnt_id):
        print(222, obj, obj_instance, prop)
        response = {}
        device = DeviceModel.find_by_bac_device_uuid(dev_uuid)
        if not device:
            abort(404, message='Device Not found')
        response['network_uuid'] = device.network.network_uuid
        response['bac_device_uuid'] = device.bac_device_uuid
        response['bac_device_mac'] = device.bac_device_mac
        response['pnt_type'] = obj
        response['pnt_id'] = obj_instance
        from bacnet.services.device import Device as DeviceService
        response['points'] = DeviceService.get_instance().get_point(device, obj, obj_instance, prop)

        return response
