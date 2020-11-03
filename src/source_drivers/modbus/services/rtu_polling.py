import time
from src import db
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.services.modbus_functions.debug import modbus_polling_count
from src.source_drivers.modbus.services.modbus_functions.polling.poll import poll_point
from src.services.event_service_base import EventServiceBase, EventTypes, Event
from src.event_dispatcher import EventDispatcher


class RtuPolling(EventServiceBase):
    _instance = None
    _polling_period = 1
    service_name = 'modbus_rtu'

    @staticmethod
    def get_instance():
        if not RtuPolling._instance:
            RtuPolling()
        return RtuPolling._instance

    def __init__(self):
        if RtuPolling._instance:
            raise Exception("MODBUS: RtuPolling class is a singleton class!")
        else:
            super().__init__()
            self.supported_events[EventTypes.INTERNAL_SERVICE_TIMEOUT] = True
            EventDispatcher.add_source_driver(self)
            RtuPolling._instance = self

    def polling(self):
        count = 0
        self.set_internal_service_timeout(RtuPolling._polling_period)
        if modbus_polling_count:
            print("RTU Polling started")
        while True:
            event = self.event_queue.get()
            if event.event_type is EventTypes.INTERNAL_SERVICE_TIMEOUT:
                count += 1
                if modbus_polling_count:
                    print(f'MODBUS: Looping RTU {count}...')

                # TODO: Implement caching
                results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
                    select_from(ModbusNetworkModel).filter_by(type=ModbusType.RTU) \
                    .join(ModbusDeviceModel).filter_by(type=ModbusType.RTU) \
                    .join(ModbusPointModel).all()

                # TODO: separate thread for each network
                ps = []
                for network, device, point in results:
                    ps.append(poll_point(network, device, point, ModbusType.RTU))

                for p in ps:
                    if p.update():
                        EventDispatcher.dispatch_from_source(self, Event(EventTypes.POINT_COV))
                db.session.commit()
                self.set_internal_service_timeout(RtuPolling._polling_period)
            else:
                raise Exception('MODBUS: unsupported event error', event.event_type)
