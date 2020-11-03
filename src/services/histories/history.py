import time

from src import db
from src.interfaces.point import HistoryType
from src.utils.model_utils import ModelUtils

from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.network.model_network import NetworkModel


class History:
    _sync_period = 5

    _instance = None
    binding = None

    def __init__(self):
        if History._instance:
            raise Exception("HISTORIES: Histories class is a singleton class!")
        else:
            History._instance = self

    @staticmethod
    def get_instance():
        if not History._instance:
            History()
        return History._instance

    def sync(self):

        while True:
            time.sleep(self._sync_period)
            for network in NetworkModel.query.all():
                for device in network.devices:
                    for point in device.points:
                        if network.history_enable and device.history_enable and point.history_enable:
                            self.sync_to_point_store_history(point)

            db.session.commit()

    def sync_to_point_store_history(self, point):
        if point.history_type == HistoryType.COV:
            point_store_history = PointStoreHistoryModel.get_latest(point.uuid)
            self.sync_on_cov(point.point_store, point_store_history)
        else:
            self.sync_on_interval(point.point_store)

    def sync_on_cov(self, point_store, point_store_history):
        print('Sync on Cov...')
        if point_store is point_store_history is None:
            difference = False
        elif not point_store_history:
            difference = True
        else:
            _point_store = ModelUtils.row2dict(point_store)
            _point_store_history = ModelUtils.row2dict(point_store_history)
            del _point_store_history['id']
            difference = _point_store != _point_store_history

        if difference:
            _point_store = ModelUtils.row2dict_default(point_store)
            _point_store_history = PointStoreHistoryModel(**_point_store)
            _point_store_history.save_to_db()

    def sync_on_interval(self, point_store):
        pass
