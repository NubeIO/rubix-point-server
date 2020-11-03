from __future__ import annotations
from src.services.event_service_base import EventServiceBase, EventTypes, Event


class EventDispatcher:

    _instance = None

    def __init__(self):
        if EventDispatcher._instance:
            raise Exception("EventDispatcher class is a singleton class!")
        else:
            EventDispatcher._instance = self
        self.services = []
        self.source_drivers = []

    @classmethod
    def get_instance(cls) -> EventDispatcher:
        if not cls._instance:
            cls()
        return cls._instance

    @classmethod
    def add_service(cls, service):
        if isinstance(service, EventServiceBase):
            cls.get_instance().services.append(service)
        else:
            raise Exception('Invalid service type added', service)

    @classmethod
    def add_source_driver(cls, driver):
        if isinstance(driver, EventServiceBase):
            cls.get_instance().source_drivers.append(driver)
        else:
            raise Exception('Invalid driver type added', driver)

    @classmethod
    def dispatch_from_source(cls, event: Event):
        for service in cls.get_instance().services:
            service.add_event(event)
