import time

import schedule
from sqlalchemy import func, and_, or_


class PointStoreCleaner:
    max_rows = 1000

    @classmethod
    def register(cls):
        print("MODBUS: Register PointStoreCleaner")
        # schedule.every(5).seconds.do(PointStoreCleaner.clean)  # for testing
        schedule.every(5).minutes.do(PointStoreCleaner.clean)  # schedules job for every hours

        while True:
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def clean(cls):
        from src import db, ModbusPointStoreModel
        print("MODBUS: Started PointStoreCleaner cleaning process...")
        time.sleep(10)
        partition_table = db.session.query(ModbusPointStoreModel, func.rank()
                                           .over(order_by=ModbusPointStoreModel.ts.desc(),
                                                 partition_by=ModbusPointStoreModel.point_uuid)
                                           .label('rank')).subquery()

        threshold_rows = db.session.query(partition_table).filter(partition_table.c.rank == cls.max_rows + 1).all()
        filter_param = []
        for threshold_row in threshold_rows:
            filter_param.append(and_(ModbusPointStoreModel.point_uuid == threshold_row.point_uuid,
                                     ModbusPointStoreModel.ts < threshold_row.ts))

        if len(filter_param) > 0:
            db.session.query(ModbusPointStoreModel).filter(or_(*filter_param)).delete()
            db.session.commit()

        print("MODBUS: Finished PointStoreCleaner cleaning process!")
