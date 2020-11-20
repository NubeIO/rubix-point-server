import time
from src import db
from src.models.network.model_network import NetworkModel
from src.models.device.model_device import DeviceModel
from src.models.point.model_point import PointModel
from src.services.event_service_base import EventServiceBase, EventTypes, Event
from src.event_dispatcher import EventDispatcher
from influxdb import InfluxDBClient

# TODO: move these to some sort of config
influx_enable = True
SERVICE_NAME_HISTORIES = 'histories'


class Histories(EventServiceBase):
    service_name = SERVICE_NAME_HISTORIES
    threaded = True
    _push_period_minutes = 1

    _instance = None
    binding = None

    def __init__(self):
        if Histories._instance:
            raise Exception("HISTORIES: Histories class is a singleton class!")
        else:
            super().__init__()
            Histories._instance = self
            self.supported_events[EventTypes.INTERNAL_SERVICE_TIMEOUT] = True
            # self.supported_events[EventTypes.POINT_COV] = True
        # TODO: create bindings

    @staticmethod
    def get_instance():
        if not Histories._instance:
            Histories()
        return Histories._instance

    def connect_binding(self):
        # TODO:
        return

    def polling(self):
        self._set_internal_service_timeout(self._push_period_minutes * 3)
        while True:
            event = self._event_queue.get()
            print('HISTORIES: event', event.event_type)
            if event.event_type is EventTypes.INTERNAL_SERVICE_TIMEOUT:
                self._set_internal_service_timeout(self._push_period_minutes * 3)

            # self.connect_binding()
            # results = self.get_points()
            # TODO: get any local histories
            # TODO: format data and post to histories
            # TODO: check post success
            #   if no, store local

    def get_points(self):
        pass
        # results = db.session.query(NetworkModel, DeviceModel, PointModel) \
        #     .select_from(PointModel) \
        #     .filter(PointModel.influx_enable == True and PointModel.enable == True) \
        #     .join(DeviceModel).filter(DeviceModel.enable == True) \
        #     .join(NetworkModel).filter(NetworkModel.enable == True) \
        #     .all()

        # return results
