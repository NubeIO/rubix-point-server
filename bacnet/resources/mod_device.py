from flask_restful import Resource, reqparse, abort, fields, marshal_with
from bacnet.models.device import DeviceModel
from bacnet.resources.network import network_fields
from bacnet.services.device import Device as DeviceService
from modbus.main import common_point_type
from bacnet.resources.interfaces.modbus_device import interface_help, interface_unit, THIS, attributes

# from bacnet.utils .data_checks import is_none


device_fields = {
    'mod_device_uuid': fields.String,
    'name': fields.String,
    'unit': fields.Integer,
    # 'timeout': fields.Integer,
    # 'ping_address': fields.Integer,
    # "ping_point_type": common_point_type['readHoldingRegisters'].String,
    # 'zeroMode': fields.Boolean,
}


class ModbusDevice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(interface_help['name'],
                        type=interface_help['type'],
                        required=interface_help['required'],
                        help=interface_help['help'],
                        )
    parser.add_argument(interface_unit['name'],
                        type=interface_unit['type'],
                        required=interface_unit['required'],
                        help=interface_unit['help'],
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = DeviceModel.find_by_bac_device_uuid(uuid)
        if not device:
            abort(404, message=f'/{THIS} not found')

        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if DeviceModel.find_by_bac_device_uuid(uuid):
            return {'message': "An device with bac_device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModbusDevice.parser.parse_args()
        device = ModbusDevice.create_device_model_obj(uuid, data)
        if device.find_by_bac_device_uuid(uuid) is not None:
            abort(409, message=f'/{THIS} already exists')
        device.save_to_db()
        return device, 201

    @marshal_with(device_fields)
    def put(self, uuid):
        data = ModbusDevice.parser.parse_args()
        device = DeviceModel.find_by_bac_device_uuid(uuid)
        if device is None:
            device = ModbusDevice.create_device_model_obj(uuid, data)
        else:
            device.name = data[attributes['name']]
            device.unit = data[attributes['unit']]
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
