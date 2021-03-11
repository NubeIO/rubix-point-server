from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.models.network import ModbusNetworkModel
from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.resources.rest_schema.schema_modbus_point import modbus_poll_non_existing_attributes, \
    point_store_fields, modbus_point_all_fields
from src.drivers.modbus.services.polling.modbus_polling import ModbusPolling
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import EventCallableBlocking


class ModbusPointPoll(RubixResource):
    @classmethod
    @marshal_with(modbus_point_all_fields)
    def get(cls, uuid: str):
        point = ModbusPointModel.find_by_uuid(uuid)
        if not point:
            raise NotFoundException('Modbus Point not found')
        else:
            event = EventCallableBlocking(ModbusPolling.poll_point, (point,))
            EventDispatcher().dispatch_to_source_only(event, Drivers.MODBUS.name)
            event.condition.wait()
            if event.error:
                raise Exception(str(event.data))
            else:
                return event.data, 200


class ModbusPointPollNonExisting(RubixResource):
    parser = reqparse.RequestParser()
    for attr in modbus_poll_non_existing_attributes:
        parser.add_argument(attr,
                            type=modbus_poll_non_existing_attributes[attr]['type'],
                            required=modbus_poll_non_existing_attributes[attr].get('required', False),
                            store_missing=False)

    @classmethod
    @marshal_with(point_store_fields)
    def post(cls):
        data = cls.parser.parse_args()
        network_data = {k.replace('network_', ''): v for k, v in data.items() if 'network_' in k}
        device_data = {k.replace('device_', ''): v for k, v in data.items() if 'device_' in k}
        point_data = {k.replace('point_', ''): v for k, v in data.items() if 'point_' in k}

        network = ModbusNetworkModel.create_temporary(**network_data)
        device = ModbusDeviceModel.create_temporary(**device_data)
        point = ModbusPointModel.create_temporary(**point_data)
        network.check_self()
        device.check_self()
        point.check_self()

        event = EventCallableBlocking(ModbusPolling.poll_point_not_existing, (point, device, network))
        EventDispatcher().dispatch_to_source_only(event, Drivers.MODBUS.name)
        event.condition.wait()
        if event.error:
            raise Exception(str(event.data))
        else:
            return event.data, 200
