import shortuuid
from flask_restful import reqparse
from rubix_http.resource import RubixResource

from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_point_all_attributes, \
    add_nested_priority_array_write
from src.models.point.priority_array import PriorityArrayModel


class ModbusPointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in modbus_point_all_attributes:
        parser.add_argument(attr,
                            type=modbus_point_all_attributes[attr]['type'],
                            required=modbus_point_all_attributes[attr].get('required', False),
                            help=modbus_point_all_attributes[attr].get('help', None),
                            store_missing=False)
    add_nested_priority_array_write()

    @classmethod
    def add_point(cls, data):
        uuid: str = shortuuid.uuid()
        priority_array_write: dict = data.pop('priority_array_write', {})
        point = ModbusPointModel(
            uuid=uuid,
            priority_array_write=PriorityArrayModel.create_priority_array_model(uuid, priority_array_write,
                                                                                data.get('fallback_value')),
            **data
        )
        point.save_to_db()
        point.publish_cov(point.point_store)
        return point
