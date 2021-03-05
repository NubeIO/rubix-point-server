import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.resources.rest_schema.schema_modbus_device import modbus_device_all_attributes, \
    modbus_device_all_fields, modbus_device_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def modbus_device_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, modbus_device_all_fields,
                                          modbus_device_all_fields_with_children)


class ModbusDeviceBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in modbus_device_all_attributes:
        parser.add_argument(attr,
                            type=modbus_device_all_attributes[attr]['type'],
                            required=modbus_device_all_attributes[attr].get('required', False),
                            help=modbus_device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_device(cls, data):
        _uuid = str(uuid.uuid4())
        device = ModbusDeviceModel(uuid=_uuid, **data)
        device.save_to_db()
        return device
