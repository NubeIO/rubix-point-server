import time

import schedule
from sqlalchemy import func, and_, or_


class PointStoreHistoryCleaner:
    MAX_ROWS = 1000

    @classmethod
    def register(cls):
        print("MODBUS: Register PointStoreHistoryCleaner")
        # schedule.every(5).seconds.do(PointStoreCleaner.clean)  # for testing
        schedule.every(5).minutes.do(PointStoreHistoryCleaner.clean)  # schedules job for every hours

        while True:
            schedule.run_pending()
            time.sleep(10)

    @classmethod
    def clean(cls):
        from src import db, PointStoreHistoryModel
        print("MODBUS: Started PointStoreHistoryCleaner cleaning process...")
        time.sleep(10)
        partition_table = db.session.query(PointStoreHistoryModel, func.rank()
                                           .over(order_by=PointStoreHistoryModel.ts.desc(),
                                                 partition_by=PointStoreHistoryModel.point_uuid)
                                           .label('rank')).subquery()

        threshold_rows = db.session.query(partition_table).filter(partition_table.c.rank == cls.MAX_ROWS + 1).all()
        filter_param = []
        for threshold_row in threshold_rows:
            filter_param.append(and_(PointStoreHistoryModel.point_uuid == threshold_row.point_uuid,
                                     PointStoreHistoryModel.ts < threshold_row.ts))

        if len(filter_param) > 0:
            db.session.query(PointStoreHistoryModel).filter(or_(*filter_param)).delete()
            db.session.commit()

        print("MODBUS: Finished PointStoreCleaner cleaning process!")
