from flask_restful import Resource, reqparse, abort, fields, marshal_with
from src.sourceDrivers.modbusCopy.models.mod_point import ModbusPointModel
# from src.sourceDrivers.modbusCopy.models. import ModbusPointModel
from src.sourceDrivers.modbusCopy.rest_schema.schema_modbus_point import point_attributes, INTERFACE_NAME


def getType(attr_type):
    if attr_type == int:
        return fields.Integer
    elif attr_type == str:
        return fields.String
    elif attr_type == bool:
        return fields.Boolean
    elif attr_type == float:
        return fields.Float


point_fields = {
    'point_value': fields.Float(attribute='value.point_value'),
}
for attr in point_attributes:
    point_fields[attr] = getType(point_attributes[attr]['type'])


class ModPoint(Resource):
    parser = reqparse.RequestParser()
    for attr in point_attributes:
        parser.add_argument(attr,
                            type=point_attributes[attr]['type'],
                            required=point_attributes[attr]['required'],
                            help=point_attributes[attr]['help'],
                            )

    @marshal_with(point_fields)
    def get(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if not point:
            abort(404, message=f'{INTERFACE_NAME} not found')
        return point

    @marshal_with(point_fields)
    def post(self, uuid):
        if ModbusPointModel.find_by_uuid(uuid):
            return {'message': "An device with mod_device_uuid '{}' already exists.".format(uuid)}, 400
        data = ModPoint.parser.parse_args()
        device = ModPoint.create_point_model_obj(uuid, data)
        if device.find_by_uuid(uuid) is not None:
            abort(409, message=f'{INTERFACE_NAME} already exists')
        device.save_to_db()
        return device, 201

    @marshal_with(point_fields)
    def put(self, uuid):
        data = ModPoint.parser.parse_args()
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            point = ModPoint.create_point_model_obj(uuid, data)
        else:
            point.point_name = data['point_name']
            point.point_enable = data['point_enable']
            point.mod_point_reg = data['mod_point_reg']
            point.mod_point_reg_length = data['mod_point_reg_length']
            point.mod_point_type = data['mod_point_type']
            point.mod_point_write_value = data['mod_point_write_value']
            point.mod_point_data_type = data['mod_point_data_type']
            point.mod_point_data_endian = data['mod_point_data_endian']
            point.mod_point_data_round = data['mod_point_data_round']
            point.mod_point_data_offset = data['mod_point_data_offset']
            point.mod_point_timeout = data['mod_point_timeout']
            point.mod_point_timeout_global = data['mod_point_timeout_global']
            point.point_prevent_duplicates = data['point_prevent_duplicates']
            point.mod_point_prevent_duplicates_global = data['point_prevent_duplicates']
            point.mod_device_uuid = data['point_device_uuid']
        point.save_to_db()
        return point

    def delete(self, uuid):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point:
            point.delete_from_db()
        return '', 204

    @staticmethod
    def create_point_model_obj(point_uuid, data):
        point = ModbusPointModel(point_uuid=point_uuid,
                                 point_name=data['point_name'],
                                 mod_point_reg=data['mod_point_reg'],
                                 mod_point_reg_length=data['mod_point_reg_length'],
                                 mod_point_type=data['mod_point_type'],
                                 point_enable=data['point_enable'],
                                 mod_point_write_value=data['mod_point_write_value'],
                                 mod_point_data_type=data['mod_point_data_type'],
                                 mod_point_data_endian=data['mod_point_data_endian'],
                                 mod_point_data_round=data['mod_point_data_round'],
                                 mod_point_data_offset=data['mod_point_data_offset'],
                                 mod_point_timeout=data['mod_point_timeout'],
                                 mod_point_timeout_global=data['mod_point_timeout_global'],
                                 point_prevent_duplicates=data['point_prevent_duplicates'],
                                 mod_point_prevent_duplicates_global=data['point_prevent_duplicates'],
                                 point_device_uuid=data['point_device_uuid'])
        # point.write_point_value(0)
        return point


class ModPointList(Resource):
    @marshal_with(point_fields, envelope="mod_points")
    def get(self):
        result = ModbusPointModel.query.all()
        return result
