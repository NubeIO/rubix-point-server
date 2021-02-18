import uuid

from flask_restful import Resource, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.resources.utils import model_network_marshaller
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_attributes, \
    modbus_network_all_fields, modbus_network_all_fields_with_children, \
    modbus_network_all_fields_without_points_children


def modbus_network_marshaller(data: any, args: dict):
    return model_network_marshaller(data, args, modbus_network_all_fields,
                                    modbus_network_all_fields_without_points_children,
                                    modbus_network_all_fields_with_children)


class ModbusNetworkBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_network_all_attributes:
        parser.add_argument(attr,
                            type=modbus_network_all_attributes[attr].get('type'),
                            required=modbus_network_all_attributes[attr].get('required', False),
                            help=modbus_network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def add_network(data):
        _uuid = str(uuid.uuid4())
        try:
            network = ModbusNetworkModel(uuid=_uuid, **data)
            network.save_to_db()
            return network
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
