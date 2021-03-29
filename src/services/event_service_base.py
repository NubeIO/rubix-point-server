import logging
from enum import IntEnum, unique, auto
from queue import Queue
from threading import Timer, Event as ThreadingEvent
from typing import Callable, List

logger = logging.getLogger(__name__)


@unique
class EventType(IntEnum):
    TEST_EVENT = 0
    INTERNAL_SERVICE_TIMEOUT = auto()
    CALLABLE = auto()
    POINT_COV = auto()
    POINT_MODEL = auto()
    DEVICE_MODEL = auto()
    NETWORK_MODEL = auto()
    NETWORK_DROPLET_MODEL = auto()
    SCHEDULE_MODEL = auto()
    MAPPING_MODEL = auto()
    MQTT_DEBUG = auto()
    POINT_REGISTRY_UPDATE = auto()
    SCHEDULES = auto()


# TODO: implement event queue overload warning and clearing
# TODO: potentially need to add thread lock to event


class HandledByDifferentServiceException(BaseException):
    def __init__(self, *args):
        super(HandledByDifferentServiceException, self).__init__(*args)


class Event:
    def __init__(self, event_type: EventType, data: any = None):
        self.event_type = event_type
        self.data = data


class EventCallableBlocking(Event):
    def __init__(self, func: Callable, args: tuple = None, kwargs=None):
        super().__init__(EventType.CALLABLE, None)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.condition = ThreadingEvent()  # could use threading.Condition to ensure exclusive access
        self.error = False


class EventServiceBase:

    def __init__(self, service_name: str, threaded: bool):
        self.service_name: str = service_name
        self.threaded: bool = threaded
        self._event_queue: Queue[Event] = Queue()
        self.supported_events: List[bool] = [False] * len(EventType)
        self._internal_timeout_thread = None

    def event_count(self):
        return self._event_queue.qsize()

    # TODO: look at way to make certain methods runnable instead of adding to thread queue if threaded service
    def add_event(self, event: Event):
        if isinstance(event, Event) and isinstance(event.event_type, EventType):
            if self.supported_events[event.event_type]:
                if self.threaded:
                    self._event_queue.put(event)
                else:
                    self._run_event(event)
        else:
            raise Exception('Tried to add invalid event: ', event)

    def _run_event(self, event: Event):
        raise Exception('_run_event() not implemented for non threaded service', self.service_name)

    def _set_internal_service_timeout(self, seconds):
        self._internal_timeout_thread = Timer(seconds, self.add_event,
                                              [Event(EventType.INTERNAL_SERVICE_TIMEOUT, None)])
        self._internal_timeout_thread.start()

    def _handle_internal_callable(self, event):
        if event.event_type is EventType.CALLABLE and isinstance(event, EventCallableBlocking):
            try:
                if event.args and event.kwargs:
                    event.data = event.func(self, *event.args, **event.kwargs)
                elif event.args:
                    event.data = event.func(self, *event.args)
                else:
                    event.data = event.func(self)
            except HandledByDifferentServiceException:
                return
            except BaseException as e:
                logger.error(e)
                event.error = True
                event.data = e

            event.condition.set()
        else:
            raise Exception(self.service_name, 'unsupported event error', event.event_type)
