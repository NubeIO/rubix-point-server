from datetime import datetime

from src import db
from src.enums.point import HistoryType
from src.handlers.exception import exception_handler
from src.models.device.model_device import DeviceModel
from src.models.network.model_network import NetworkModel
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.services.event_service_base import EventServiceBase, EventType
from src.utils import Singleton
from src.utils.model_utils import get_datetime

SERVICE_NAME_HISTORIES_LOCAL = 'histories_local'


class HistoryLocal(EventServiceBase, metaclass=Singleton):
    """
    A simple history saving protocol for those points which has `history_type=INTERVAL`
    """
    SYNC_PERIOD = 5

    binding = None

    def __init__(self):
        super().__init__(SERVICE_NAME_HISTORIES_LOCAL, True)
        self.supported_events[EventType.INTERNAL_SERVICE_TIMEOUT] = True

    def sync_interval(self):
        from src.event_dispatcher import EventDispatcher
        EventDispatcher().add_service(self)
        while True:
            self._set_internal_service_timeout(self.SYNC_PERIOD)
            event = self._event_queue.get()
            if event.event_type is not EventType.INTERNAL_SERVICE_TIMEOUT:
                raise Exception('History Local: invalid event received somehow... should be impossible')
            results = self.__get_all_enabled_interval_points()
            for point, point_store in results:
                latest_point_store_history: PointStoreHistoryModel = PointStoreHistoryModel.get_latest(point.uuid)
                self.__sync_on_interval(point, point_store, latest_point_store_history)

            db.session.commit()

    @staticmethod
    def __get_all_enabled_interval_points():
        return db.session.query(PointModel, PointStoreModel).select_from(PointModel) \
            .filter_by(history_enable=True, history_type=HistoryType.INTERVAL) \
            .join(DeviceModel).filter_by(history_enable=True) \
            .join(NetworkModel).filter_by(history_enable=True) \
            .join(PointStoreModel) \
            .all()

    @staticmethod
    @exception_handler
    def __sync_on_interval(point: PointModel, point_store: PointStoreModel,
                           latest_point_store_history: PointStoreHistoryModel):
        if not point_store.ts_value:
            """This means we don't have real value till now"""
            return
        current_dt: datetime = get_datetime()
        if not latest_point_store_history:
            """Minutes is placing such a way if 15, then it will store values on 0, 15, 30, 45"""
            minute: int = int(current_dt.minute / point.history_interval) * point.history_interval
            point_store.ts_value = point_store.ts_value.replace(minute=minute, second=0, microsecond=0)
            PointStoreHistoryModel.create_history(point_store)
        elif (current_dt - latest_point_store_history.ts_value).total_seconds() >= point.history_interval * 60:
            """Minutes is placing such a way if 15, then it will store values on 0, 15, 30, 45"""
            minute: int = int(current_dt.minute / point.history_interval) * point.history_interval
            current_dt = current_dt.replace(minute=minute, second=0, microsecond=0)
            point_store.ts_value = current_dt
            PointStoreHistoryModel.create_history(point_store)
