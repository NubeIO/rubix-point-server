from src import db
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import EventServiceBase, EventTypes
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel, ModbusType
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.services.modbus_functions.debug import modbus_debug_poll, modbus_polling_count
from src.source_drivers.modbus.services.modbus_functions.polling.poll import poll_point

SERVICE_NAME_MODBUS_TCP = 'modbus_tcp'


class TcpPolling(EventServiceBase):
    _instance = None
    _polling_period = 1
    service_name = SERVICE_NAME_MODBUS_TCP
    _count = 0

    @staticmethod
    def get_instance():
        if not TcpPolling._instance:
            TcpPolling()
        return TcpPolling._instance

    def __init__(self):
        if TcpPolling._instance:
            raise Exception("TcpPolling class is a singleton class!")
        else:
            super().__init__()
            self.supported_events[EventTypes.INTERNAL_SERVICE_TIMEOUT] = True
            self.supported_events[EventTypes.CALLABLE] = True
            EventDispatcher.add_source_driver(self)
            TcpPolling._instance = self

    def polling(self):
        self._set_internal_service_timeout(TcpPolling._polling_period)
        if modbus_debug_poll:
            print("MODBUS TCP Polling started")
        while True:
            event = self._event_queue.get()
            if event.event_type is EventTypes.INTERNAL_SERVICE_TIMEOUT:
                self.__poll()
                self._set_internal_service_timeout(TcpPolling._polling_period)
            else:
                self._handle_internal_callable(event)

    def __poll(self):
        self._count += 1
        if modbus_polling_count:
            print(f'Looping TCP {self._count}...')
        results = self.__get_all_points()
        # TODO: separate thread for each network
        for network, device, point in results:
            if all(v is not None for v in results):
                poll_point(self, network, device, point, ModbusType.TCP)
        db.session.commit()

    def __get_all_points(self):
        results = db.session.query(ModbusNetworkModel, ModbusDeviceModel, ModbusPointModel). \
            select_from(ModbusNetworkModel).filter_by(type=ModbusType.TCP, enable=True) \
            .join(ModbusDeviceModel).filter_by(type=ModbusType.TCP, enable=True) \
            .join(ModbusPointModel).filter_by(enable=True).all()
        return results
