from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes


class ModbusDeviceBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        parser.add_argument(attr,
                            type=modbus_device_all_attributes[attr]['type'],
                            required=modbus_device_all_attributes[attr].get('required', False),
                            help=modbus_device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_device_model_obj(uuid, data):
        return ModbusDeviceModel(uuid=uuid, **data)

    @classmethod
    def add_device(cls, uuid, data):
        try:
            device = ModbusDeviceBase.create_device_model_obj(uuid, data)
            device.save_to_db()
            return device
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
