from flask_restful import Resource, reqparse, abort, marshal_with

from src.modbus.interfaces.device.interface_modbus_device import attributes, THIS, \
    interface_mod_device_name, \
    interface_mod_device_enable, interface_mod_device_type, \
    interface_mod_device_addr, interface_mod_tcp_device_ip, \
    interface_mod_tcp_device_port, interface_mod_ping_point_type, \
    interface_mod_ping_point_address, interface_mod_device_zero_mode, \
    interface_mod_device_timeout, interface_mod_device_timeout_global, interface_mod_network_uuid
from src.modbus.models.mod_device import ModbusDeviceModel
from src.modbus.resources.mod_fields import device_fields


class ModDevice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(interface_mod_device_name['name'],
                        type=interface_mod_device_name['type'],
                        required=interface_mod_device_name['required'],
                        help=interface_mod_device_name['help'],
                        )
    parser.add_argument(interface_mod_device_enable['name'],
                        type=interface_mod_device_enable['type'],
                        required=interface_mod_device_enable['required'],
                        help=interface_mod_device_enable['help'],
                        )
    parser.add_argument(interface_mod_device_type['name'],
                        type=interface_mod_device_type['type'],
                        required=interface_mod_device_type['required'],
                        help=interface_mod_device_type['help'],
                        )
    parser.add_argument(interface_mod_device_addr['name'],
                        type=interface_mod_device_addr['type'],
                        required=interface_mod_device_addr['required'],
                        help=interface_mod_device_addr['help'],
                        )
    parser.add_argument(interface_mod_tcp_device_ip['name'],
                        type=interface_mod_tcp_device_ip['type'],
                        required=interface_mod_tcp_device_ip['required'],
                        help=interface_mod_tcp_device_ip['help'],
                        )
    parser.add_argument(interface_mod_tcp_device_port['name'],
                        type=interface_mod_tcp_device_port['type'],
                        required=interface_mod_tcp_device_port['required'],
                        help=interface_mod_tcp_device_port['help'],
                        )
    parser.add_argument(interface_mod_ping_point_type['name'],
                        type=interface_mod_ping_point_type['type'],
                        required=interface_mod_ping_point_type['required'],
                        help=interface_mod_ping_point_type['help'],
                        )
    parser.add_argument(interface_mod_ping_point_address['name'],
                        type=interface_mod_ping_point_address['type'],
                        required=interface_mod_ping_point_address['required'],
                        help=interface_mod_ping_point_address['help'],
                        )
    parser.add_argument(interface_mod_device_zero_mode['name'],
                        type=interface_mod_device_zero_mode['type'],
                        required=interface_mod_device_zero_mode['required'],
                        help=interface_mod_device_zero_mode['help'],
                        )
    parser.add_argument(interface_mod_device_timeout['name'],
                        type=interface_mod_device_timeout['type'],
                        required=interface_mod_device_timeout['required'],
                        help=interface_mod_device_timeout['help'],
                        )
    parser.add_argument(interface_mod_device_timeout_global['name'],
                        type=interface_mod_device_timeout_global['type'],
                        required=interface_mod_device_timeout_global['required'],
                        help=interface_mod_device_timeout_global['help'],
                        )
    parser.add_argument(interface_mod_network_uuid['name'],
                        type=interface_mod_network_uuid['type'],
                        required=interface_mod_network_uuid['required'],
                        help=interface_mod_network_uuid['help'],
                        )

    @marshal_with(device_fields)
    def get(self, uuid):
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if not device:
            abort(404, message=f'{THIS} not found')

        return device

    @marshal_with(device_fields)
    def post(self, uuid):
        if ModbusDeviceModel.find_by_device_uuid(uuid):
            return {'message': "An device with mod_device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModDevice.parser.parse_args()
        try:
            device = ModDevice.create_device_model_obj(uuid, data)
            if device.find_by_device_uuid(uuid) is not None:
                abort(409, message=f'{THIS} already exists')
            device.save_to_db()
            return device, 201
        except Exception as e:
            return abort(500, message=str(e))

    @marshal_with(device_fields)
    def put(self, uuid):
        data = ModDevice.parser.parse_args()
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if device is None:
            try:
                device = ModDevice.create_device_model_obj(uuid, data)
            except Exception as e:
                return abort(500, message=str(e))
        else:
            device.mod_device_name = data[attributes['mod_device_name']]
            device.mod_device_enable = data[attributes['mod_device_enable']]
            device.mod_device_type = data[attributes['mod_device_type']]
            device.mod_device_addr = data[attributes['mod_device_addr']]
            device.mod_tcp_device_ip = data[attributes['mod_tcp_device_ip']]
            device.mod_tcp_device_port = data[attributes['mod_tcp_device_port']]
            device.mod_ping_point_type = data[attributes['mod_ping_point_type']]
            device.mod_ping_point_address = data[attributes['mod_ping_point_address']]
            device.mod_device_zero_mode = data[attributes['mod_device_zero_mode']]
            device.mod_device_timeout = data[attributes['mod_device_timeout']]
            device.mod_device_timeout_global = data[attributes['mod_device_timeout_global']]
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(mod_device_uuid, data):
        return ModbusDeviceModel(mod_device_uuid=mod_device_uuid,
                                 mod_device_name=data['mod_device_name'],
                                 mod_device_enable=data['mod_device_enable'],
                                 mod_device_type=data['mod_device_type'],
                                 mod_device_addr=data['mod_device_addr'],
                                 mod_tcp_device_ip=data['mod_tcp_device_ip'],
                                 mod_tcp_device_port=data['mod_tcp_device_port'],
                                 mod_ping_point_type=data['mod_ping_point_type'],
                                 mod_ping_point_address=data['mod_ping_point_address'],
                                 mod_device_zero_mode=data['mod_device_zero_mode'],
                                 mod_device_timeout=data['mod_device_timeout'],
                                 mod_device_timeout_global=data['mod_device_timeout_global'],
                                 mod_network_uuid=data['mod_network_uuid'])


class ModDeviceList(Resource):
    @marshal_with(device_fields, envelope="mod_devices")
    def get(self):
        return ModbusDeviceModel.query.all()
