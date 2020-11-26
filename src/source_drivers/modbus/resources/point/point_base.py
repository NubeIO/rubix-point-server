from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_attributes
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode, ModbusDataType


class ModbusPointBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        parser.add_argument(attr,
                            type=modbus_point_all_attributes[attr]['type'],
                            required=modbus_point_all_attributes[attr].get('required', False),
                            help=modbus_point_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_point_model_obj(uuid, data):
        return ModbusPointModel(uuid=uuid, **data)

    @classmethod
    def add_point(cls, data, uuid):
        try:
            # cls.validate_modbus_point_json(data)
            point = ModbusPointBase.create_point_model_obj(uuid, data)
            point.save_to_db()
            return point
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))

    # @staticmethod
    # def validate_modbus_point_json(data: dict):
    #     # TODO: take point obj to allow for patch on existing fields that are missing from data

        # point_fc = data.get('function_code')
        # reg_length = data.get('register_length')
        #
        # if point_fc is not None and reg_length is not None:
        #     point_fc = ModbusFunctionCode[data.get('function_code')]
        #     reg_length = int(data.get('register_length'))
        #     if point_fc == ModbusFunctionCode.WRITE_COIL or point_fc == ModbusFunctionCode.WRITE_REGISTER \
        #             or point_fc == ModbusFunctionCode.WRITE_COILS or point_fc == ModbusFunctionCode.WRITE_REGISTERS:
        #         data['writable'] = True
        #         if data.get('write_value') is None:
        #             data['write_value'] = 0.0
        #
        #         if reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_COIL:
        #             data['function_code'] = ModbusFunctionCode.WRITE_COILS
        #         elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_COILS:
        #             data['function_code'] = ModbusFunctionCode.WRITE_COIL
        #         elif reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_REGISTER:
        #             data['function_code'] = ModbusFunctionCode.WRITE_REGISTERS
        #         elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_REGISTERS:
        #             data['function_code'] = ModbusFunctionCode.WRITE_REGISTER
        #
        #     elif point_fc == ModbusFunctionCode.READ_COILS or point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS or \
        #             point_fc == ModbusFunctionCode.READ_HOLDING_REGISTERS or \
        #             point_fc == ModbusFunctionCode.READ_INPUT_REGISTERS:
        #         data['writable'] = False
        #         data['write_value'] = None
        #
        #     data_type = ModbusDataType[data.get('data_type')]
        #     if point_fc is not None or data_type is not None:
        #         if point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS or point_fc == ModbusFunctionCode.READ_COILS or \
        #                 point_fc == ModbusFunctionCode.WRITE_COIL or point_fc == ModbusFunctionCode.WRITE_COILS:
        #             data_type = ModbusDataType.DIGITAL
        #             data['data_type'] = ModbusDataType.DIGITAL
        #             data['data_round'] = 0
        #
        #         if data_type == ModbusDataType.FLOAT or data_type == ModbusDataType.INT32 or \
        #                 data_type == ModbusDataType.UINT32:
        #             assert reg_length % 2 == 0, f'register_length invalid for data_type {data_type}'
