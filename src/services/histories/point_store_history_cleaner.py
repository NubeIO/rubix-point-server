import logging
from datetime import datetime, timedelta

import gevent
from sqlalchemy import func, and_

from src.handlers.exception import exception_handler
from src.setting import CleanerSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class PointStoreHistoryCleaner(metaclass=Singleton):
    def __init__(self):
        self.__config = None

    @property
    def config(self) -> CleanerSetting:
        return self.__config

    def setup(self, config: CleanerSetting):
        logger.info("Register PointStoreHistoryCleaner")
        self.__config = config
        while True:
            gevent.sleep(self.config.frequency * 60)
            self.clean()

    @exception_handler
    def clean(self):
        from src import db
        from src.models.point.model_point_store_history import PointStoreHistoryModel
        latest_point_id_rows = db.session.query(
            PointStoreHistoryModel,
            func.max(PointStoreHistoryModel.id).label('id')
        ).group_by(PointStoreHistoryModel.point_uuid).all()
        latest_point_ids = list(map(lambda x: x.id, latest_point_id_rows))
        persistence_ts = datetime.utcnow() - timedelta(hours=self.config.data_persisting_hours)
        db.session.query(PointStoreHistoryModel).filter(
            and_((PointStoreHistoryModel.ts_value < persistence_ts),
                 ~PointStoreHistoryModel.id.in_(latest_point_ids))).delete()
        db.session.commit()
        logger.info("Finished PointStoreCleaner cleaning process!")
