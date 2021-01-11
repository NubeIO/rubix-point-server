from src.services.event_service_base import EventServiceBase, Event
from src.utils import Singleton


class EventDispatcher(metaclass=Singleton):

    def __init__(self):
        self.__services = []
        self.__source_drivers = []

    def add_service(self, service: EventServiceBase):
        if isinstance(service, EventServiceBase):
            self.__services.append(service)
        else:
            raise Exception('Invalid service type added', service)

    def add_source_driver(self, new_driver: EventServiceBase):
        if not isinstance(new_driver, EventServiceBase):
            raise Exception('Invalid driver type added', new_driver)
        else:
            for driver in self.__source_drivers:
                if driver == new_driver:
                    raise Exception('driver already registered:', new_driver)
            self.__source_drivers.append(new_driver)

    def dispatch_from_service(self, origin_service: EventServiceBase, event: Event, source_driver_name: str = None):
        self.dispatch_to_source_only(event, source_driver_name)
        for service in self.__services:
            if service is not origin_service:
                service.add_event(event)

    def dispatch_to_source_only(self, event: Event, source_driver_name: str = None):
        if source_driver_name:
            for driver in self.__source_drivers:
                if driver.service_name == source_driver_name:
                    driver.add_event(event)

    def dispatch_from_source(self, origin_source_driver: EventServiceBase or None, event: Event):
        for service in self.__services:
            service.add_event(event)
