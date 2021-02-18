from flask_restful import Resource, reqparse, marshal_with, abort

from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import EventCallableBlocking
from src.source_drivers import MODBUS_SERVICE_NAME
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_point import modbud_poll_non_existing_attributes, \
    point_store_fields, modbus_point_all_fields
from src.source_drivers.modbus.services import ModbusPolling


class ModbusPointPoll(Resource):
    @classmethod
    @marshal_with(modbus_point_all_fields)
    def get(cls, uuid: str):
        point = ModbusPointModel.find_by_uuid(uuid)
        if point is None:
            abort(404, message=f'Modbus Point not found')
        else:
            event = EventCallableBlocking(ModbusPolling.poll_point, (point,))
            EventDispatcher().dispatch_to_source_only(event, MODBUS_SERVICE_NAME)
            event.condition.wait()
            if event.error:
                abort(500, message=str(event.data))
            else:
                return event.data, 200


class ModbusPointPollNonExisting(Resource):
    parser = reqparse.RequestParser()
    for attr in modbud_poll_non_existing_attributes:
        parser.add_argument(attr,
                            type=modbud_poll_non_existing_attributes[attr]['type'],
                            required=modbud_poll_non_existing_attributes[attr].get('required', False),
                            store_missing=False)

    @classmethod
    @marshal_with(point_store_fields)
    def post(cls):
        data = cls.parser.parse_args()
        network_data = {k.replace('network_', ''): v for k, v in data.items() if 'network_' in k}
        device_data = {k.replace('device_', ''): v for k, v in data.items() if 'device_' in k}
        point_data = {k.replace('point_', ''): v for k, v in data.items() if 'point_' in k}
        network = None
        device = None
        point = None
        try:
            network = ModbusNetworkModel.create_temporary(**network_data)
            device = ModbusDeviceModel.create_temporary(**device_data)
            point = ModbusPointModel.create_temporary(**point_data)
            network.check_self()
            device.check_self()
            point.check_self()
        except Exception as e:
            abort(500, message=str(e))

        event = EventCallableBlocking(ModbusPolling.poll_point_not_existing, (point, device, network))
        EventDispatcher().dispatch_to_source_only(event, MODBUS_SERVICE_NAME)
        event.condition.wait()
        if event.error:
            abort(500, message=str(event.data))
        else:
            return event.data, 200

# from src.event_dispatcher import EventDispatcher
# from src.services.event_service_base import Event, EventCallableBlocking, EventType
# from src.source_drivers.modbus.services.rtu_polling import RtuPolling
#
#
# class TestEndPoint(Resource):
#
#     @classmethod
#     def get(cls, thing):
#         event = EventCallableBlocking(RtuPolling.temporary_test_func, (thing, thing))
#         EventDispatcher.dispatch_to_source_only(
#             event, 'modbus_rtu')
#         event.condition.wait()
#         if event.error:
#             abort(500, message='unknown error')
#         else:
#             return event.data, 200
