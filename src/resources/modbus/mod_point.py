from flask_restful import Resource, reqparse, abort, fields, marshal_with
from src.models.modbus.mod_point import ModbusPointModel
from src.interfaces.modbus.point.interface_modbus_point import points_attributes, THIS, interface_name, interface_reg, \
    interface_reg_length, interface_point_type, interface_point_enable, interface_point_write_value, \
    interface_point_data_type, interface_point_data_endian, interface_point_data_round, interface_point_data_offset, \
    interface_point_timeout, interface_point_timeout_global, interface_point_prevent_duplicates, \
    interface_point_prevent_duplicates_global, interface_interface_help_device_uuid

fields = {
    'mod_point_uuid': fields.String,
    'mod_point_name': fields.String,
    'mod_point_reg': fields.Integer,
    'mod_point_reg_length': fields.Integer,
    'mod_point_type': fields.String,
    'mod_point_enable': fields.Boolean,
    'mod_point_write_value': fields.Integer,
    'mod_point_data_type': fields.String,
    'mod_point_data_endian': fields.String,
    'mod_point_data_round': fields.Integer,
    'mod_point_data_offset': fields.Integer,
    'mod_point_timeout': fields.Integer,
    'mod_point_timeout_global': fields.Boolean,
    'mod_point_prevent_duplicates': fields.Boolean,
    'mod_point_prevent_duplicates_global': fields.Boolean,
    'mod_device_uuid': fields.String,
}


class ModPoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(interface_name['name'],
                        type=interface_name['type'],
                        required=interface_name['required'],
                        help=interface_name['help'],
                        )
    parser.add_argument(interface_reg['name'],
                        type=interface_reg['type'],
                        required=interface_reg['required'],
                        help=interface_reg['help'],
                        )
    parser.add_argument(interface_reg_length['name'],
                        type=interface_reg_length['type'],
                        required=interface_reg_length['required'],
                        help=interface_reg_length['help'],
                        )
    parser.add_argument(interface_point_type['name'],
                        type=interface_point_type['type'],
                        required=interface_point_type['required'],
                        help=interface_point_type['help'],
                        )
    parser.add_argument(interface_point_enable['name'],
                        type=interface_point_enable['type'],
                        required=interface_point_enable['required'],
                        help=interface_point_enable['help'],
                        )
    parser.add_argument(interface_point_write_value['name'],
                        type=interface_point_write_value['type'],
                        required=interface_point_write_value['required'],
                        help=interface_point_write_value['help'],
                        )
    parser.add_argument(interface_point_data_type['name'],
                        type=interface_point_data_type['type'],
                        required=interface_point_data_type['required'],
                        help=interface_point_data_type['help'],
                        )
    parser.add_argument(interface_point_data_endian['name'],
                        type=interface_point_data_endian['type'],
                        required=interface_point_data_endian['required'],
                        help=interface_point_data_endian['help'],
                        )
    parser.add_argument(interface_point_data_round['name'],
                        type=interface_point_data_round['type'],
                        required=interface_point_data_round['required'],
                        help=interface_point_data_round['help'],
                        )
    parser.add_argument(interface_point_data_offset['name'],
                        type=interface_point_data_offset['type'],
                        required=interface_point_data_offset['required'],
                        help=interface_point_data_offset['help'],
                        )
    parser.add_argument(interface_point_timeout['name'],
                        type=interface_point_timeout['type'],
                        required=interface_point_timeout['required'],
                        help=interface_point_timeout['help'],
                        )
    parser.add_argument(interface_point_timeout_global['name'],
                        type=interface_point_timeout_global['type'],
                        required=interface_point_timeout_global['required'],
                        help=interface_point_timeout_global['help'],
                        )
    parser.add_argument(interface_point_prevent_duplicates['name'],
                        type=interface_point_prevent_duplicates['type'],
                        required=interface_point_prevent_duplicates['required'],
                        help=interface_point_prevent_duplicates['help'],
                        )
    parser.add_argument(interface_point_prevent_duplicates_global['name'],
                        type=interface_point_prevent_duplicates_global['type'],
                        required=interface_point_prevent_duplicates_global['required'],
                        help=interface_point_prevent_duplicates_global['help'],
                        )
    parser.add_argument(interface_interface_help_device_uuid['name'],
                        type=interface_interface_help_device_uuid['type'],
                        required=interface_interface_help_device_uuid['required'],
                        help=interface_interface_help_device_uuid['help'],
                        )

    @marshal_with(fields)
    def get(self, uuid):
        device = ModbusPointModel.find_by_uuid(uuid)
        if not device:
            abort(404, message=f'{THIS} not found')
        return device

    @marshal_with(fields)
    def post(self, uuid):
        if ModbusPointModel.find_by_uuid(uuid):
            return {'message': "An device with mod_device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModPoint.parser.parse_args()
        device = ModPoint.create_point_model_obj(uuid, data)
        if device.find_by_uuid(uuid) is not None:
            abort(409, message=f'{THIS} already exists')
        device.save_to_db()
        return device, 201

    @marshal_with(fields)
    def put(self, uuid):
        data = ModPoint.parser.parse_args()
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            point = ModPoint.create_point_model_obj(uuid, data)
        else:
            point.mod_point_name = data[points_attributes['mod_point_name']]
            point.mod_point_reg = data[points_attributes['mod_point_reg']]
            point.mod_point_reg_length = data[points_attributes['mod_point_reg_length']]
            point.mod_point_type = data[points_attributes['mod_point_type']]
            point.mod_point_enable = data[points_attributes['mod_point_enable']]
            point.mod_point_write_value = data[points_attributes['mod_point_write_value']]
            point.mod_point_data_type = data[points_attributes['mod_point_data_type']]
            point.mod_point_data_endian = data[points_attributes['mod_point_data_endian']]
            point.mod_point_data_round = data[points_attributes['mod_point_data_round']]
            point.mod_point_data_offset = data[points_attributes['mod_point_data_offset']]
            point.mod_point_timeout = data[points_attributes['mod_point_timeout']]
            point.mod_point_timeout_global = data[points_attributes['mod_point_timeout_global']]
            point.mod_point_prevent_duplicates = data[points_attributes['mod_point_prevent_duplicates']]
            point.mod_point_prevent_duplicates_global = data[points_attributes['mod_point_prevent_duplicates_global']]
            point.mod_device_uuid = data[points_attributes['mod_device_uuid']]
        point.save_to_db()
        return point

    def delete(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204

    @staticmethod
    def create_point_model_obj(mod_point_uuid, data):
        return ModbusPointModel(mod_point_uuid=mod_point_uuid, mod_point_name=data['mod_point_name'],
                                mod_point_reg=data['mod_point_reg'], mod_point_reg_length=data['mod_point_reg_length'],
                                mod_point_type=data['mod_point_type'], mod_point_enable=data['mod_point_enable'],
                                mod_point_write_value=data['mod_point_write_value'],
                                mod_point_data_type=data['mod_point_data_type'],
                                mod_point_data_endian=data['mod_point_data_endian'],
                                mod_point_data_round=data['mod_point_data_round'],
                                mod_point_data_offset=data['mod_point_data_offset'],
                                mod_point_timeout=data['mod_point_timeout'],
                                mod_point_timeout_global=data['mod_point_timeout_global'],
                                mod_point_prevent_duplicates=data['mod_point_prevent_duplicates'],
                                mod_point_prevent_duplicates_global=data['mod_point_prevent_duplicates_global'],
                                mod_device_uuid=data['mod_device_uuid'])


class ModPointList(Resource):
    @marshal_with(fields, envelope="mod_points")
    def get(self):
        return ModbusPointModel.query.all()

# mod_device_point_fields = network_fields
# mod_updated_device_fields = fields.copy()
# mod_updated_device_fields.update({'hello': fields.String})
# mod_device_point_fields['points'] = fields.List(fields.Nested(mod_updated_device_fields))
