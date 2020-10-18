from flask_restful import Resource, reqparse, abort, fields, marshal_with
from bacnet.models.mod_device import ModDeviceModel
from bacnet.resources.mod_network import network_fields
from bacnet.interfaces.modbus.modbus_device import interface_name, interface_ip, interface_port, attributes, THIS

# from modnet.utils .data_checks import is_none


device_fields = {
    'mod_device_uuid': fields.String,
    'mod_device_name': fields.String,
    'mod_device_ip': fields.String,
    'mod_device_port': fields.Integer,
    # 'ping_address': fields.Integer,
    # "ping_point_type": common_point_type['readHoldingRegisters'].String,
    # 'zeroMode': fields.Boolean,
}


class ModDevice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(interface_name['name'],
                        type=interface_name['type'],
                        required=interface_name['required'],
                        help=interface_name['help'],
                        )
    parser.add_argument(interface_ip['name'],
                        type=interface_ip['type'],
                        required=interface_ip['required'],
                        help=interface_ip['help'],
                        )
    parser.add_argument(interface_port['name'],
                        type=interface_port['type'],
                        required=interface_port['required'],
                        help=interface_port['help'],
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = ModDeviceModel.find_by_device_uuid(uuid)
        if not device:
            abort(404, message=f'{THIS} not found')

        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if ModDeviceModel.find_by_device_uuid(uuid):
            return {'message': "An device with mod_device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModDevice.parser.parse_args()
        device = ModDevice.create_device_model_obj(uuid, data)
        if device.find_by_device_uuid(uuid) is not None:
            abort(409, message=f'{THIS} already exists')
        device.save_to_db()
        return device, 201

    @marshal_with(device_fields)
    def put(self, uuid):
        data = ModDevice.parser.parse_args()
        device = ModDeviceModel.find_by_device_uuid(uuid)
        if device is None:
            device = ModDevice.create_device_model_obj(uuid, data)
        else:
            device.mod_device_name = data[attributes['mod_device_name']]
            device.mod_device_ip = data[attributes['mod_device_ip']]
            device.mod_device_port = data[attributes['mod_device_port']]
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = ModDeviceModel.find_by_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(mod_device_uuid, data):
        return ModDeviceModel(mod_device_uuid=mod_device_uuid, mod_device_name=data['mod_device_name'], mod_device_ip=data['mod_device_ip'], mod_device_port=data['mod_device_port'])


class ModDeviceList(Resource):
    @marshal_with(device_fields, envelope="mod_devices")
    def get(self):
        return ModDeviceModel.query.all()


mod_device_point_fields = network_fields
mod_updated_device_fields = device_fields.copy()
mod_updated_device_fields.update({'hello': fields.String})
mod_device_point_fields['devices'] = fields.List(fields.Nested(mod_updated_device_fields))
