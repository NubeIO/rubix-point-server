from flask_restful import Resource, reqparse, fields, marshal_with, abort
from src.resources.utils import mapRestSchema
from src.sourceDrivers.modbusCopy.models.mod_network import ModbusNetworkModel
from src.sourceDrivers.modbusCopy.rest_schema.schema_modbus_network import modbus_network_all_attributes, \
    network_return_attributes


modbus_network_all_fields = {}
mapRestSchema(modbus_network_all_attributes, modbus_network_all_fields)
mapRestSchema(network_return_attributes, modbus_network_all_fields)


class ModNetwork(Resource):
    parser = reqparse.RequestParser()
    for attr in modbus_network_all_attributes:
        parser.add_argument(attr,
                            type=modbus_network_all_attributes[attr]['type'],
                            required=modbus_network_all_attributes[attr]['required'],
                            help=modbus_network_all_attributes[attr]['help'],
                            )

    @marshal_with(modbus_network_all_fields)
    def get(self, uuid):
        network = ModbusNetworkModel.find_by_network_uuid(uuid)
        if not network:
            abort(404, message='Modbus Network not found')
        return network

    @marshal_with(modbus_network_all_fields)
    def post(self, uuid):
        print('POST NETWORK')
        print('finding existing...')
        if ModbusNetworkModel.find_by_network_uuid(uuid):
            return abort(409, message=f"An Modbus Network with network_uuid '{uuid}' already exists.")
        print('no existing')
        data = ModNetwork.parser.parse_args()
        try:
            print('creating model')
            network = ModNetwork.create_network_model_obj(uuid, data)
            print('saving model')
            network.save_to_db()
            return network, 201
        except Exception as e:
            return abort(500, message=str(e))

    # @marshal_with(modbus_network_all_fields)
    # def put(self, uuid):
    #     data = ModNetwork.parser.parse_args()
    #     network = ModbusNetworkModel.find_by_network_uuid(uuid)
    #     if network is None:
    #         try:
    #             network = ModNetwork.create_network_model_obj(uuid, data)
    #         except Exception as e:
    #             return abort(500, message=str(e))
    #     else:
    #         network.network_name = data['network_name']
    #         network.mod_network_port = data['network_enable']
    #         network.mod_network_type = data['mod_network_type']
    #         network.mod_network_port = data['mod_network_timeout']
    #         network.mod_network_port = data['mod_network_device_timeout_global']
    #         network.mod_network_port = data['mod_network_point_timeout_global']
    #         network.mod_network_port = data['mod_rtu_network_port']
    #         network.mod_network_port = data['mod_rtu_network_speed']
    #         network.mod_network_port = data['mod_rtu_network_stopbits']
    #         network.mod_network_port = data['mod_rtu_network_parity']
    #         network.mod_network_port = data['mod_rtu_network_bytesize']
    #     network.save_to_db()
    #     return network, 201
    #
    # def delete(self, uuid):
    #     network_uuid = uuid
    #     network = ModbusNetworkModel.find_by_network_uuid(network_uuid)
    #     if network:
    #         network.delete_from_db()
    #     return '', 204

    @staticmethod
    def create_network_model_obj(network_uuid, data):
        return ModbusNetworkModel(network_uuid=network_uuid,
                                  network_name=data['network_name'],
                                  mod_network_type=data['mod_network_type'],
                                  network_enable=data['network_enable'],
                                  mod_network_timeout=data['mod_network_timeout'],
                                  mod_network_device_timeout_global=data['mod_network_device_timeout_global'],
                                  mod_network_point_timeout_global=data['mod_network_point_timeout_global'],
                                  mod_rtu_network_port=data['mod_rtu_network_port'],
                                  mod_rtu_network_speed=data['mod_rtu_network_speed'],
                                  mod_rtu_network_stopbits=data['mod_rtu_network_stopbits'],
                                  mod_rtu_network_parity=data['mod_rtu_network_parity'],
                                  mod_rtu_network_bytesize=data['mod_rtu_network_bytesize'])


class ModNetworkList(Resource):
    @marshal_with(modbus_network_all_fields, envelope="modbus_networks")
    def get(self):
        return ModbusNetworkModel.query.all()


class ModNetworksIds(Resource):
    @marshal_with(modbus_network_all_fields, envelope="modbus_network_uuids")
    def get(self):
        return ModbusNetworkModel.query.all()
