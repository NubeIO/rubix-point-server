import logging
import time

import psycopg2
import schedule
from psycopg2.extras import execute_values
from registry.registry import RubixRegistry

from src.handlers.exception import exception_handler
from src.models.point.model_point import PointModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
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
                                             sslmode=self.config.ssl_mode, connect_timeout=self.config.connect_timeout)
            self.__is_connected = True
            self._create_table_if_not_exists()
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        logger.info('PostgreSQL sync has is been called')
        self.__wires_plat = RubixRegistry().read_wires_plat()
        if not self.__wires_plat:
            logger.error('Please add wires-plat on Rubix Service')
            return
        self._sync()

    def _sync(self):
        data_detail = []
        data_history = []
        for point in PointModel.find_all():
            point_last_sync_id: int = self._get_point_last_sync_id(point.uuid)
            for psh in PointStoreHistoryModel.get_all_after(point_last_sync_id, point.uuid):
                point_store_history: PointStoreHistoryModel = psh
                point: PointModel = point_store_history.point
                detail = (point.uuid, point.name,
                          self.__wires_plat.get('client_id'), self.__wires_plat.get('client_name'),
                          self.__wires_plat.get('site_id'), self.__wires_plat.get('site_name'),
                          self.__wires_plat.get('device_id'), self.__wires_plat.get('device_name'),
                          point.device.uuid, point.device.name, point.device.network.uuid, point.device.network.name,
                          point.driver)

                data_detail.append(detail)
                history = (point_store_history.id, point_store_history.point_uuid, point_store_history.value,
                           point_store_history.value_original, point_store_history.value_raw, point_store_history.fault,
                           point_store_history.fault_message, point_store_history.ts_value,
                           point_store_history.ts_fault)
                data_history.append(history)
        if len(data_history):
            logger.debug(f"Storing data_detail: {data_detail}")
            logger.debug(f"Storing data_history: {data_history}")
            query_details = f'INSERT INTO {self.config.table_name}_details (point_uuid,point_name,client_id ,' \
                            f'client_name,site_id,site_name,device_id,device_name,edge_device_uuid,edge_device_name,' \
                            f'network_uuid,network_name,driver) VALUES %s ON CONFLICT (point_uuid) DO UPDATE SET ' \
                            f'point_name = excluded.point_name, client_id = excluded.client_id, client_name = ' \
                            f'excluded.client_name, site_id = excluded.site_id,site_name = excluded.site_name, ' \
                            f'device_id = excluded.device_id, device_name = excluded.device_name, edge_device_uuid = ' \
                            f'excluded.edge_device_uuid, edge_device_name = excluded.edge_device_name, network_uuid = ' \
                            f'excluded.network_uuid, network_name = excluded.network_name, driver = excluded.driver '
            query_histories = f'INSERT INTO {self.config.table_name} (id,point_uuid,value,value_original,value_raw,' \
                              f'fault,fault_message,ts_value,ts_fault) VALUES %s ON CONFLICT (id) DO NOTHING'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_details, list(set(data_detail)))
                        execute_values(curs, query_histories, data_history)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored {len(data_detail)} rows on {self.config.table_name}_details table')
            logger.info(f'Stored {len(list(set(data_detail)))} rows on {self.config.table_name} table')
        else:
            logger.debug("Nothing to store, no new records")

    def _create_table_if_not_exists(self):
        query_details = f'CREATE TABLE IF NOT EXISTS {self.config.table_name}_details (point_uuid VARCHAR ' \
                        f'PRIMARY KEY,point_name VARCHAR(80),client_id VARCHAR(80),client_name VARCHAR(80),' \
                        f'site_id VARCHAR(80),site_name VARCHAR(80),device_id VARCHAR(80),device_name VARCHAR(80),' \
                        f'edge_device_uuid VARCHAR(80),edge_device_name VARCHAR(80),network_uuid VARCHAR(80),' \
                        f'network_name VARCHAR(80),driver VARCHAR(80)); '
        query_history = f'CREATE TABLE IF NOT EXISTS {self.config.table_name} (id INTEGER PRIMARY KEY,point_uuid ' \
                        f'VARCHAR REFERENCES {self.config.table_name}_details ON DELETE RESTRICT,value NUMERIC,' \
                        f'value_original NUMERIC,value_raw VARCHAR,fault BOOLEAN,fault_message VARCHAR,ts_value ' \
                        f'TIMESTAMP,ts_fault TIMESTAMP,CONSTRAINT fk_{self.config.table_name}_details FOREIGN KEY(' \
                        f'point_uuid) REFERENCES {self.config.table_name}_details(point_uuid));'
        with self.__client:
            with self.__client.cursor() as curs:
                try:
                    curs.execute(query_details)
                    curs.execute(query_history)
                except psycopg2.Error as e:
                    logger.error(str(e))

    def _get_point_last_sync_id(self, point_uuid):
        query = f"SELECT MAX(id) FROM {self.config.table_name} WHERE point_uuid=%s;"
        with self.__client:
            with self.__client.cursor() as curs:
                curs.execute(query, (point_uuid,))
                last_sync_id = curs.fetchone()[0]
                if last_sync_id:
                    return last_sync_id
                return 0
