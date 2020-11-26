from flask_restful import Resource, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_network import modbus_network_all_attributes


class ModbusNetworkBase(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_network_all_attributes:
        parser.add_argument(attr,
                            type=modbus_network_all_attributes[attr].get('type'),
                            required=modbus_network_all_attributes[attr].get('required', False),
                            help=modbus_network_all_attributes[attr].get('help', None),
                            store_missing=False)

    @staticmethod
    def create_network_model_obj(uuid, data):
        return ModbusNetworkModel(uuid=uuid, **data)

    @staticmethod
    def add_network(uuid, data):
        try:
            network = ModbusNetworkBase.create_network_model_obj(uuid, data)
            network.save_to_db()
            return network
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))
