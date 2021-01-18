from logging import StreamHandler

from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import Event, EventType


class MqttStreamHandler(StreamHandler):

    def emit(self, record):
        try:
            msg = self.format(record)
            event = Event(EventType.MQTT_DEBUG, msg)
            # TODO: better use of dispatching
            EventDispatcher().dispatch_from_service(None, event, None)
        except Exception as e:
            event = Event(EventType.MQTT_DEBUG, str(e))
            EventDispatcher().dispatch_from_service(None, event, None)
