import time
from src import db
from src.models.network.model_network import NetworkModel
from src.models.device.model_device import DeviceModel
from src.models.point.model_point import PointModel
from influxdb import InfluxDBClient

# TODO: move these to some sort of config
influx_enable = True


class Histories:

    _push_period_minutes = 1

    _instance = None
    binding = None

    def __init__(self):
        if Histories._instance:
            raise Exception("HISTORIES: Histories class is a singleton class!")
        else:
            Histories._instance = self
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
        while True:
            time.sleep(self._push_period_minutes * 60)
            self.connect_binding()
            #
            results = self.get_points()
            # TODO: get any local histories
            # TODO: format data and post to histories
            # TODO: check post success
            #   if no, store local

    def get_points(self):
        results = db.session.query(NetworkModel, DeviceModel, PointModel) \
            .select_from(PointModel) \
            .filter(PointModel.influx_enable == True and PointModel.enable == True) \
            .join(DeviceModel).filter(DeviceModel.enable == True) \
            .join(NetworkModel).filter(NetworkModel.enable == True) \
            .all()

        return results
