import time
from src import db
from src.models.network.model_network import NetworkModel
from src.models.device.model_device import DeviceModel
from src.models.point.model_point import PointModel
from influxdb import InfluxDBClient


class Influx:

    _push_period_minutes = 1

    _instance = None
    _client = None

    host = None
    port = None
    database_name = None
    username = None
    password = None

    def __init__(self):
        if Influx._instance:
            raise Exception("INFLUX: Influx class is a singleton class!")
        else:
            Influx._instance = self

    @staticmethod
    def get_instance():
        if not Influx._instance:
            Influx()
        return Influx._instance

    def connect_client(self):
        # TODO: check client already connected
        # self._client = InfluxDBClient(self.host, self.port, self.username, self.password, self.database_name)
        return

    def polling(self):
        while True:
            time.sleep(self._push_period_minutes * 60)
            if self._client is None:  # or Influx._client is not connected?
                self.connect_client()
                # TODO: handle connection failed

            #
            results = self.get_points()
            # TODO: format data and post to influx

    def get_points(self):
        results = db.session.query(NetworkModel, DeviceModel, PointModel) \
            .select_from(PointModel) \
            .filter(PointModel.influx_enable == True and PointModel.enable == True) \
            .join(DeviceModel).filter(DeviceModel.enable == True) \
            .join(NetworkModel).filter(NetworkModel.enable == True) \
            .all()

        return results

    def post_points(self, point_data):
        # point_data should contain all point data
        # push to influx
        return

    def post_point_single(self, point_data):
        # This will potentially be used for COV events
        return