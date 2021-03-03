import json
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
        point_list = []
        point_value_data_list = []
        point_tag_list = []
        for point in PointModel.find_all():
            point_last_sync_id: int = self._get_point_last_sync_id(point.uuid)
            for psh in PointStoreHistoryModel.get_all_after(point_last_sync_id, point.uuid):
                point_store_history: PointStoreHistoryModel = psh
                point: PointModel = point_store_history.point
                _point = (point.uuid, point.name,
                          self.__wires_plat.get('client_id'), self.__wires_plat.get('client_name'),
                          self.__wires_plat.get('site_id'), self.__wires_plat.get('site_name'),
                          self.__wires_plat.get('device_id'), self.__wires_plat.get('device_name'),
                          point.device.uuid, point.device.name, point.device.network.uuid, point.device.network.name,
                          point.driver)

                point_list.append(_point)
                point_value_data = (point_store_history.id, point_store_history.point_uuid, point_store_history.value,
                                    point_store_history.value_original, point_store_history.value_raw,
                                    point_store_history.fault, point_store_history.fault_message,
                                    point_store_history.ts_value, point_store_history.ts_fault)
                point_value_data_list.append(point_value_data)

                if point.tags:
                    point_tags = json.loads(point.tags)
                    # insert tags from point object
                    for point_tag in point_tags:
                        point_tag_list.append(point.uuid, point_tag, point_tags[point_tag])
        if len(point_value_data_list):
            logger.debug(f"Storing point_list: {point_list}")
            logger.debug(f"Storing point_value_data_list: {point_value_data_list}")
            logger.debug(f"Storing point_tag_list: {point_tag_list}")
            query_point = f'INSERT INTO {self.config.table_name} (point_uuid,point_name,client_id ,' \
                          f'client_name,site_id,site_name,device_id,device_name,edge_device_uuid,edge_device_name,' \
                          f'network_uuid,network_name,driver) VALUES %s ON CONFLICT (point_uuid) DO UPDATE SET ' \
                          f'point_name = excluded.point_name, client_id = excluded.client_id, client_name = ' \
                          f'excluded.client_name, site_id = excluded.site_id,site_name = excluded.site_name, ' \
                          f'device_id = excluded.device_id, device_name = excluded.device_name, edge_device_uuid = ' \
                          f'excluded.edge_device_uuid, edge_device_name = excluded.edge_device_name, network_uuid = ' \
                          f'excluded.network_uuid, network_name = excluded.network_name, driver = excluded.driver '
            query_point_value_data = f'INSERT INTO {self.config.table_name}_value_data (id,point_uuid,value,' \
                                     f'value_original,value_raw,fault,fault_message,ts_value,ts_fault) ' \
                                     f'VALUES %s ON CONFLICT (id) DO NOTHING'
            query_point_tag = f'INSERT INTO {self.config.table_name}_tag (point_uuid,tag_name,tag_value) VALUES %s ' \
                              f'ON CONFLICT (point_uuid,tag_name) DO UPDATE SET tag_value = excluded.tag_value'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_point, list(set(point_list)))
                        execute_values(curs, query_point_value_data, point_value_data_list)
                        if len(point_tag_list):
                            query_delete_point_tag = f'DELETE FROM {self.config.table_name}_tag WHERE point_uuid IN ' \
                                                     f'{tuple(i[0] for i in point_tag_list)} AND ' \
                                                     f'(point_uuid,tag_name) NOT IN ' \
                                                     f'{tuple((i[0], i[1]) for i in point_tag_list)}'
                            curs.execute(query_delete_point_tag)
                        execute_values(curs, query_point_tag, point_tag_list)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored {len(point_list)} rows on {self.config.table_name} table')
            logger.info(f'Stored {len(list(set(point_value_data_list)))} rows on {self.config.table_name}_value_data '
                        f'table')
            logger.info(f'Stored {len(point_tag_list)} rows on {self.config.table_name}_tag table')
        else:
            logger.debug("Nothing to store, no new records")

    def _create_table_if_not_exists(self):
        query_point = f'CREATE TABLE IF NOT EXISTS {self.config.table_name} (point_uuid VARCHAR PRIMARY KEY,' \
                      f'point_name VARCHAR(80),client_id VARCHAR(80),client_name VARCHAR(80),site_id VARCHAR(80),' \
                      f'site_name VARCHAR(80),device_id VARCHAR(80),device_name VARCHAR(80),' \
                      f'edge_device_uuid VARCHAR(80),edge_device_name VARCHAR(80),network_uuid VARCHAR(80),' \
                      f'network_name VARCHAR(80),driver VARCHAR(80));'
        query_point_value_data = f'CREATE TABLE IF NOT EXISTS {self.config.table_name}_value_data ' \
                                 f'(id INTEGER PRIMARY KEY,point_uuid VARCHAR REFERENCES ' \
                                 f'{self.config.table_name} ON DELETE RESTRICT,value NUMERIC,' \
                                 f'value_original NUMERIC,value_raw VARCHAR,fault BOOLEAN,fault_message VARCHAR,' \
                                 f'ts_value  TIMESTAMP,ts_fault TIMESTAMP,' \
                                 f'CONSTRAINT fk_{self.config.table_name} FOREIGN KEY(point_uuid) ' \
                                 f'REFERENCES {self.config.table_name}(point_uuid));'
        query_point_tag = f'CREATE TABLE IF NOT EXISTS {self.config.table_name}_tag (point_uuid VARCHAR REFERENCES ' \
                          f'{self.config.table_name} ON DELETE RESTRICT, tag_name VARCHAR, tag_value VARCHAR,' \
                          f'PRIMARY KEY (point_uuid, tag_name));'
        with self.__client:
            with self.__client.cursor() as curs:
                try:
                    curs.execute(query_point)
                    curs.execute(query_point_value_data)
                    curs.execute(query_point_tag)
                except psycopg2.Error as e:
                    logger.error(str(e))

    def _get_point_last_sync_id(self, point_uuid):
        query = f"SELECT MAX(id) FROM {self.config.table_name}_value_data WHERE point_uuid=%s;"
        with self.__client:
            with self.__client.cursor() as curs:
                curs.execute(query, (point_uuid,))
                last_sync_id = curs.fetchone()[0]
                if last_sync_id:
                    return last_sync_id
                return 0
