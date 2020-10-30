from flask_restful import Resource, reqparse, abort

from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes


class ModbusDeviceBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        parser.add_argument(attr,
                            type=modbus_device_all_attributes[attr]['type'],
                            required=modbus_device_all_attributes[attr]['required'],
                            help=modbus_device_all_attributes[attr]['help'],
                            )

    @staticmethod
    def create_device_model_obj(uuid, data):
        return ModbusDeviceModel(uuid=uuid, **data)

    @classmethod
    def add_device(cls, uuid, data):
        cls.abort_if_network_does_not_exist_and_type_mismatch(data.network_uuid, data.type)
        try:
            device = ModbusDeviceBase.create_device_model_obj(uuid, data)
            device.save_to_db()
            return device
        except Exception as e:
            abort(500, message=str(e))

    @staticmethod
    def abort_if_network_does_not_exist_and_type_mismatch(network_uuid, type):
        network = ModbusNetworkModel.find_by_uuid(network_uuid)
        if not network:
            abort(400, message='Network does not exist of that network_uuid')
        if network.type.name != type:
            abort(400, message=f'Type Mismatch: network.type is `{network.type}` and device.type needs to be same')
