import time
from datetime import datetime

from src import db
from src.interfaces.point import HistoryType
from src.models.network.model_network import NetworkModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.utils.model_utils import ModelUtils


class HistoryInterval:
    """
    A simple history saving protocol for those points which has `history_type=INTERVAL`
    """
    SYNC_PERIOD = 5

    _instance = None
    binding = None

    def __init__(self):
        if HistoryInterval._instance:
            raise Exception("HISTORY SYNC: HistoryInterval class is a singleton class!")
        else:
            HistoryInterval._instance = self

    @staticmethod
    def get_instance():
        if not HistoryInterval._instance:
            HistoryInterval()
        return HistoryInterval._instance

    def sync_interval(self):
        while True:
            time.sleep(self.SYNC_PERIOD)
            for network in NetworkModel.query.all():
                for device in network.devices:
                    for point in device.points:
                        if network.history_enable and device.history_enable and point.history_enable:
                            self.sync_to_point_store_history(point)

            db.session.commit()

    def sync_to_point_store_history(self, point):
        latest_point_store_history = PointStoreHistoryModel.get_latest(point.uuid)
        if point.history_type == HistoryType.INTERVAL:
            self.sync_on_interval(point, latest_point_store_history)

    def sync_on_interval(self, point, latest_point_store_history):
        point_store = point.point_store
        if not latest_point_store_history:
            # minutes is placing such a way if 15, then it will store values on 0, 15, 30, 45
            minute = int(datetime.utcnow().minute / point.history_interval) * point.history_interval
            point_store.ts = point_store.ts.replace(minute=minute, second=0, microsecond=0)
            self.save_point_store_history(point_store)
        elif (datetime.utcnow() - latest_point_store_history.ts).total_seconds() >= point.history_interval * 60:
            point_store.ts = datetime.utcnow().replace(second=0, microsecond=0)
            self.save_point_store_history(point_store)

    def save_point_store_history(self, point_store):
        _point_store = ModelUtils.row2dict_default(point_store)
        _point_store_history = PointStoreHistoryModel(**_point_store)
        _point_store_history.save_to_db()
