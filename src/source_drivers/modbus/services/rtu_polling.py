from src import db
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import EventServiceBase, EventTypes
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.services.modbus_functions.debug import modbus_debug_poll, modbus_polling_count
from src.source_drivers.modbus.services.modbus_functions.polling.poll import poll_point

SERVICE_NAME_MODBUS_RTU = 'modbus_rtu'


class RtuPolling(EventServiceBase):
    _instance = None
    _polling_period = 1
    service_name = SERVICE_NAME_MODBUS_RTU
    _count = 0

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
            self.supported_events[EventTypes.CALLABLE] = True
            EventDispatcher.add_source_driver(self)
            RtuPolling._instance = self

    def polling(self):
        self._set_internal_service_timeout(RtuPolling._polling_period)
        if modbus_debug_poll:
            print("RTU Polling started")
        while True:
            event = self._event_queue.get()
            if event.event_type is EventTypes.INTERNAL_SERVICE_TIMEOUT:
                self.__poll()
                self._set_internal_service_timeout(RtuPolling._polling_period)
            else:
                self._handle_internal_callable(event)

    def __poll(self):
        self._count += 1
        if modbus_polling_count:
            print(f'MODBUS: Looping RTU {self._count}...')

        results = self.__get_all_points()
        # TODO: separate thread for each network
        for network, device, point in results:
            if all(v is not None for v in results):
                poll_point(self, network, device, point, ModbusType.RTU)
        db.session.commit()

    def __get_all_points(self):
        results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
            select_from(ModbusNetworkModel).filter_by(type=ModbusType.RTU, enable=True) \
            .join(ModbusDeviceModel).filter_by(type=ModbusType.RTU, enable=True) \
            .join(ModbusPointModel).filter_by(enable=True).all()
        return results
