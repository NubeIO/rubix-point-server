from flask_restful import Resource, reqparse, abort, fields, marshal_with
from src.resources.utils import mapRestSchema
from src.sourceDrivers.modbusCopy.models.mod_device import ModbusDeviceModel
from src.sourceDrivers.modbusCopy.rest_schema.schema_modbus_device import modbus_device_all_attributes, \
    device_return_attributes, INTERFACE_NAME


modbus_device_all_fields = {}
mapRestSchema(modbus_device_all_attributes, modbus_device_all_fields)
mapRestSchema(device_return_attributes, modbus_device_all_fields)


class ModDevice(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        parser.add_argument(attr,
                            type=modbus_device_all_attributes[attr]['type'],
                            required=modbus_device_all_attributes[attr]['required'],
                            help=modbus_device_all_attributes[attr]['help'],
                            )

    @marshal_with(modbus_device_all_fields)
    def get(self, uuid):
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if not device:
            abort(404, message=f'{INTERFACE_NAME} not found')

        return device

    @marshal_with(modbus_device_all_fields)
    def post(self, uuid):
        if ModbusDeviceModel.find_by_device_uuid(uuid):
            return {'message': "An device with device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModDevice.parser.parse_args()
        try:
            device = ModDevice.create_device_model_obj(uuid, data)
            if device.find_by_device_uuid(uuid) is not None:
                abort(409, message=f'{INTERFACE_NAME} already exists')
            device.save_to_db()
            return device, 201
        except Exception as e:
            return abort(500, message=str(e))

    @marshal_with(modbus_device_all_fields)
    def put(self, uuid):
        data = ModDevice.parser.parse_args()
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if device is None:
            try:
                device = ModDevice.create_device_model_obj(uuid, data)
            except Exception as e:
                return abort(500, message=str(e))
        else:
            device.device_name = data['device_name']
            device.device_enable = data['device_enable']
            device.mod_device_type = data['mod_device_type']
            device.mod_device_addr = data['mod_device_addr']
            device.mod_tcp_device_ip = data['mod_tcp_device_ip']
            device.mod_tcp_device_port = data['mod_tcp_device_port']
            device.mod_ping_point_type = data['mod_ping_point_type']
            device.mod_ping_point_address = data['mod_ping_point_address']
            device.mod_device_zero_mode = data['mod_device_zero_mode']
            device.mod_device_timeout = data['mod_device_timeout']
            device.mod_device_timeout_global = data['mod_device_timeout_global']
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = ModbusDeviceModel.find_by_device_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_device_model_obj(device_uuid, data):
        return ModbusDeviceModel(device_uuid=device_uuid,
                                 device_name=data['device_name'],
                                 device_enable=data['device_enable'],
                                 mod_device_type=data['mod_device_type'],
                                 mod_device_addr=data['mod_device_addr'],
                                 mod_tcp_device_ip=data['mod_tcp_device_ip'],
                                 mod_tcp_device_port=data['mod_tcp_device_port'],
                                 mod_ping_point_type=data['mod_ping_point_type'],
                                 mod_ping_point_address=data['mod_ping_point_address'],
                                 mod_device_zero_mode=data['mod_device_zero_mode'],
                                 mod_device_timeout=data['mod_device_timeout'],
                                 mod_device_timeout_global=data['mod_device_timeout_global'],
                                 device_network_uuid=data['device_network_uuid'])


class ModDeviceList(Resource):
    @marshal_with(modbus_device_all_fields, envelope="modbus_devices")
    def get(self):
        return ModbusDeviceModel.query.all()
