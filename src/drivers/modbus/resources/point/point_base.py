import uuid

from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_attributes
from src.models.point.priority_array import PriorityArrayModel


class ModbusPointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        parser.add_argument(attr,
                            type=modbus_point_all_attributes[attr]['type'],
                            required=modbus_point_all_attributes[attr].get('required', False),
                            help=modbus_point_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_point(cls, data):
        _uuid = str(uuid.uuid4())
        point = ModbusPointModel(uuid=_uuid, **data)
        point.priority_array_write = PriorityArrayModel.create_new_priority_array_model(_uuid)
        point.save_to_db()
        return point
