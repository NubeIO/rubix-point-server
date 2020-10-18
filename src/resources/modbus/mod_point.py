from flask_restful import Resource, reqparse, abort, fields, marshal_with
from src.models.modbus.mod_point import ModbusPointModel
# from src.resources.modbus.mod_network import network_fields
from src.interfaces.modbus.point.interface_modbus_point import interface_name, interface_reg, attributes, THIS


fields = {
    'mod_point_uuid': fields.String,
    'mod_point_name': fields.String,
    'mod_point_reg': fields.String,
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
        device = ModbusPointModel.find_by_uuid(uuid)
        if device is None:
            device = ModPoint.create_point_model_obj(uuid, data)
        else:
            device.mod_point_name = data[attributes['mod_point_name']]
            device.mod_point_reg = data[attributes['mod_point_reg']]
        device.save_to_db()
        return device

    def delete(self, uuid):
        device = ModbusPointModel.find_by_uuid(uuid)
        if device:
            device.delete_from_db()
        return '', 204

    @staticmethod
    def create_point_model_obj(mod_point_uuid, data):
        return ModbusPointModel(mod_point_uuid=mod_point_uuid, mod_point_name=data['mod_point_name'], mod_point_reg=data['mod_point_reg'])


class ModPointList(Resource):
    @marshal_with(fields, envelope="mod_points")
    def get(self):
        return ModbusPointModel.query.all()


# mod_device_point_fields = network_fields
# mod_updated_device_fields = fields.copy()
# mod_updated_device_fields.update({'hello': fields.String})
# mod_device_point_fields['points'] = fields.List(fields.Nested(mod_updated_device_fields))
