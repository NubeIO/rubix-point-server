from queue import Queue
from enum import IntEnum, unique, auto
from threading import Timer


@unique
class EventTypes(IntEnum):
    INTERNAL_SERVICE_TIMEOUT = 0
    POINT_COV = auto()
    # POINT_WRITE = auto()
    # POINT_UPDATE = auto()
    # DEVICE_UPDATE = auto()
    # NETWORK_UPDATE = auto()


class Event:

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data


class EventServiceBase:

    def __init__(self):
        self.event_queue = Queue()
        self.supported_events = [False] * len(EventTypes)
        self.internal_timeout_thread = None

    def add_event(self, event):
        if isinstance(event, Event) and isinstance(event.event_type, EventTypes):
            if self.supported_events[event.event_type]:
                self.event_queue.put(event)
        else:
            raise Exception('Tried to add bad event: ', event)

    def set_internal_service_timeout(self, seconds):
        self.internal_timeout_thread = Timer(seconds, self.add_event,
                                             [Event(EventTypes.INTERNAL_SERVICE_TIMEOUT, None)])
        self.internal_timeout_thread.start()
