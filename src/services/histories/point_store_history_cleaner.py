import logging
import time

import schedule
from sqlalchemy import func, and_, or_

from src.utils import Singleton

logger = logging.getLogger(__name__)


class PointStoreHistoryCleaner(metaclass=Singleton):
    MAX_ROWS = 1000

    def __init__(self):
        self.config = None

    # TODO: add config here e.g: trigger frequency
    def setup(self):
        logger.info("Register PointStoreHistoryCleaner")
        # schedule.every(5).seconds.do(PointStoreCleaner.clean)  # for testing
        schedule.every(5).minutes.do(self.clean)  # schedules job for every hours
        while True:
            schedule.run_pending()
            time.sleep(10)

    def clean(self):
        from src import db
        from src.models.point.model_point_store_history import PointStoreHistoryModel
        logger.info("Started PointStoreHistoryCleaner cleaning process...")
        time.sleep(10)
        partition_table = db.session.query(PointStoreHistoryModel, func.rank()
                                           .over(order_by=PointStoreHistoryModel.ts_value.desc(),
                                                 partition_by=PointStoreHistoryModel.point_uuid)
                                           .label('rank')).subquery()

        threshold_rows = db.session.query(partition_table).filter(partition_table.c.rank == self.MAX_ROWS + 1).all()
        filter_param = []
        for threshold_row in threshold_rows:
            filter_param.append(and_(PointStoreHistoryModel.point_uuid == threshold_row.point_uuid,
                                     PointStoreHistoryModel.ts_value < threshold_row.ts_value))

        if len(filter_param) > 0:
            db.session.query(PointStoreHistoryModel).filter(or_(*filter_param)).delete()
            db.session.commit()

        logger.info("Finished PointStoreCleaner cleaning process!")
