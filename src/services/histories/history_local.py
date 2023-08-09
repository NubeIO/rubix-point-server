import logging
import time
from datetime import datetime

from flask import current_app
from gevent import sleep

from src import db, AppSetting
from src.enums.point import HistoryType
from src.handlers.exception import exception_handler
from src.models.device.model_device import DeviceModel
from src.models.network.model_network import NetworkModel
from src.models.point.model_point import PointModel
from src.models.point.model_point_store import PointStoreModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.utils import Singleton, dbsession
from src.utils.model_utils import get_datetime

SERVICE_NAME_HISTORIES_LOCAL = 'histories_local'

logger = logging.getLogger(__name__)


class HistoryLocal(metaclass=Singleton):
    """
    A simple history saving protocol for those points which has `history_type=INTERVAL`
    """
    binding = None

    def sync_interval(self):
        setting: AppSetting = current_app.config[AppSetting.KEY]
        while True:
            sleep(setting.services.history_create_loop_frequency_secs)
            logger.info("HistoryLocal > sync_interval is started...")
            self.__sync_interval()
            logger.info("HistoryLocal > sync_interval is ended...")

    @exception_handler
    def __sync_interval(self):
        with db.session.no_autoflush:
            results = self.__get_all_enabled_interval_points()
            i = 0
            for point, point_store in results:
                if i % 10 == 0:
                    time.sleep(0.01)
                latest_point_store_history: PointStoreHistoryModel = PointStoreHistoryModel.get_latest(point.uuid)
                self.__sync_on_interval(point, point_store, latest_point_store_history)
                i += 1
        dbsession.commit(db)

    @staticmethod
    def __get_all_enabled_interval_points():
        return db.session.query(PointModel, PointStoreModel).select_from(PointModel) \
            .filter_by(history_enable=True) \
            .filter((PointModel.history_type == HistoryType.COV_AND_INTERVAL) |
                    (PointModel.history_type == HistoryType.INTERVAL)) \
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
