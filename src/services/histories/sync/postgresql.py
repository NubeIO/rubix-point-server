import logging
import time

import psycopg2
import schedule

from src.handlers.exception import exception_handler
from src.models.point.model_point import PointModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.wires.model_wires_plat import WiresPlatModel
from src.services.histories.history_binding import HistoryBinding
from src.setting import PostgresSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class PostgreSQL(HistoryBinding, metaclass=Singleton):

    def __init__(self):
        self.__config = None
        self.__client = None
        self.__wires_plat = None
        self.__is_connected = False

    @property
    def config(self) -> PostgresSetting:
        return self.__config

    def status(self) -> bool:
        return self.__is_connected

    def disconnect(self):
        self.__is_connected = False

    def setup(self, config: PostgresSetting):
        self.__config = config
        while not self.status():
            self.connect()
            time.sleep(self.config.attempt_reconnect_secs)
        if self.status():
            logger.info("Registering PostgreSQL for scheduler job")
            # schedule.every(5).seconds.do(self.sync)  # for testing
            schedule.every(self.config.timer).minutes.do(self.sync)
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            logger.error("PostgreSQL can't be registered with not working client details")

    def connect(self):
        if self.__client:
            self.__client.close()
        try:
            self.__client = psycopg2.connect(host=self.config.host, port=self.config.port, dbname=self.config.dbname,
                                             user=self.config.user, password=self.config.password,
                                             sslmode=self.config.ssl_mode, onnect_timeout=self.config.connect_timeout)
            self.__is_connected = True
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        logger.info('PostgreSQL sync has is been called')
        self.__wires_plat = WiresPlatModel.find_one()
        if not self.__wires_plat:
            logger.error("Please add wires-plat")
        else:
            self._sync()

    def _sync(self):
        store = []
        for point in PointModel.find_all():
            point_last_sync_id: int = self._get_point_last_sync_id(point.uuid)
            for psh in PointStoreHistoryModel.get_all_after(point_last_sync_id, point.uuid):
                point_store_history: PointStoreHistoryModel = psh
                query = f'INSERT INTO {self.config.table_name} (id,point_uuid,value,value_original,value_raw,fault,' \
                        f'fault_message,ts_value,ts_fault) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                data = (point_store_history.id, point_store_history.point_uuid, point_store_history.value,
                        point_store_history.value_original, point_store_history.value_raw, point_store_history.fault,
                        point_store_history.fault_message, point_store_history.ts_value, point_store_history.ts_fault)
                with self.__client:
                    with self.__client.cursor() as curs:
                        curs.execute(query, data)
                row = {
                    'table': 'history',
                    'time': point_store_history.ts_value,
                    'fields': point_store_history
                }
                store.append(row)
        if len(store):
            logger.debug(f"Storing: {store}")
            self.__client.write_points(store)
            logger.info(f'Stored {len(store)} rows on {self.config.table_name} table')
        else:
            logger.debug("Nothing to store, no new records")

    def _get_point_last_sync_id(self, point_uuid):
        query = f"SELECT MAX(id) FROM {self.config.table_name} WHERE point_id=%s;"
        with self.__client:
            with self.__client.cursor() as curs:
                curs.execute(query, (point_uuid, ))
                last_sync_id = curs.fetchone()[0]
                if last_sync_id:
                    return last_sync_id
                return 0
