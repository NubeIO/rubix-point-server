import json
import logging
import time
from typing import List, Union

import gevent
import psycopg2
from psycopg2.extras import execute_values
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info

from src.enums.driver import Drivers
from src.enums.history_sync import HistorySyncType
from src.handlers.exception import exception_handler
from src.models.device.model_device import DeviceModel
from src.models.history_sync.model_history_sync_detail import HistorySyncDetailModel
from src.models.history_sync.model_history_sync_log import HistorySyncLogModel
from src.models.network.model_network import NetworkModel
from src.models.point.model_point import PointModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.services.histories.history_binding import HistoryBinding
from src.setting import PostgresSetting
from src.utils import Singleton
from src.utils.string import rreplace

logger = logging.getLogger(__name__)

PAGE_SIZE: int = 100

device_info: Union[DeviceInfoModel, None] = get_device_info()


class PostgreSQL(HistoryBinding, metaclass=Singleton):

    def __init__(self):
        self.__config: Union[PostgresSetting, None] = None
        self.__client = None
        self.__is_connected = False
        self.__device_info_table_name: str = ''
        self.__networks_table_name: str = ''
        self.__devices_table_name: str = ''
        self.__points_table_name: str = ''
        self.__points_values_table_name: str = ''
        self.__points_tags_table_name: str = ''
        self.__networks_tags_table_name: str = ''
        self.__devices_tags_table_name: str = ''
        self.__postgres_details: str = ''
        self.__postgres_details_changed: bool = False

    @property
    def config(self) -> Union[PostgresSetting, None]:
        return self.__config

    def status(self) -> bool:
        return self.__is_connected and self.__client and not self.__client.closed

    def disconnect(self):
        self.__is_connected = False

    def setup(self, config: PostgresSetting):
        self.__config = config
        self.__device_info_table_name: str = f'{self.config.table_prefix}_wires_plats'
        self.__networks_table_name: str = f'{self.config.table_prefix}_networks'
        self.__devices_table_name: str = f'{self.config.table_prefix}_devices'
        self.__points_table_name: str = f'{self.config.table_prefix}_points'
        self.__points_values_table_name: str = f'{self.__points_table_name}_values'
        self.__devices_tags_table_name: str = f'{self.__devices_table_name}_tags'
        self.__networks_tags_table_name: str = f'{self.__networks_table_name}_tags'
        self.__points_tags_table_name: str = f'{self.__points_table_name}_tags'
        self.__postgres_details: str = f'{self.config.host}:{self.config.port}:{self.config.dbname}:' \
                                       f'{self.__points_values_table_name}'
        self.__postgres_details_changed = HistorySyncDetailModel.find_details_by_type(
            HistorySyncType.POSTGRES.name) != self.__postgres_details
        while not self.status():
            self.connect()
            time.sleep(self.config.attempt_reconnect_secs)
        if self.status():
            logger.info("Registering PostgreSQL for sync job")
            while True:
                gevent.sleep(self.config.timer * 60)
                self.sync()
        else:
            logger.error("PostgreSQL can't be registered with not working client details")

    def connect(self):
        if self.__client:
            self.__client.close()
        try:
            self.__client = psycopg2.connect(host=self.config.host,
                                             port=self.config.port,
                                             dbname=self.config.dbname,
                                             user=self.config.user,
                                             password=self.config.password,
                                             sslmode=self.config.ssl_mode,
                                             connect_timeout=self.config.connect_timeout)
            self.__is_connected = True
            self._create_table_if_not_exists()
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        logger.info('PostgreSQL sync has is been called')
        if not device_info:
            logger.error('Please add device-info on Rubix Service')
            return
        self._sync()

    def _sync(self):
        points_list: List[tuple] = []
        points_values_list: List[tuple] = []
        points_tags_list: List[tuple] = []
        history_sync_log_list: List[dict] = []
        for point in PointModel.find_all():
            if not self.status():  # reconnect in case of postgres connection gets down
                self.connect()
            point_last_sync_id: Union[int, None] = self._get_point_last_sync_id(point.uuid)
            if not self.status() or point_last_sync_id is None:
                return
            _point: tuple = (point.device.uuid, point.uuid, point.name, Drivers.GENERIC.name)
            points_list.append(_point)
            if point.tags:
                point_tags: dict = json.loads(point.tags)
                # insert tags from point object
                for point_tag in point_tags.keys():
                    points_tags_list.append((point.uuid, point_tag, point_tags[point_tag]))
            point_store_histories = PointStoreHistoryModel.get_all_after(point_last_sync_id, point.uuid)
            for psh in point_store_histories:
                point_store_history: PointStoreHistoryModel = psh
                point_value_data: tuple = (point_store_history.id, point_store_history.point_uuid,
                                           point_store_history.value, point_store_history.value_original,
                                           point_store_history.value_raw,
                                           point_store_history.fault, point_store_history.fault_message,
                                           point_store_history.ts_value, point_store_history.ts_fault)
                points_values_list.append(point_value_data)
            if point_store_histories:
                history_sync_log = {'type': HistorySyncType.POSTGRES.name,
                                    'point_uuid': point.uuid,
                                    'last_sync_id': point_store_histories[-1].id}
                history_sync_log_list.append(history_sync_log)
            gevent.sleep(0.1)  # it becomes heavy on single loop, so being idle for some time to give other process time
        logger.info("Sync service bulk data has been created...")
        try:
            self._update_device_info()
        except Exception as e:
            logger.error(f'Error: {e}')
            self.connect()
            return
        self._update_networks()
        self._update_networks_tags()
        self._update_devices()
        self._update_devices_tags()
        self._update_points_list(points_list)
        self._update_points_values(points_values_list)
        self._update_points_tags(points_tags_list)
        if len(history_sync_log_list):
            HistorySyncLogModel.update_history_sync_logs(history_sync_log_list)
            if self.__postgres_details_changed:
                HistorySyncDetailModel.update_history_sync_details(
                    {'type': HistorySyncType.POSTGRES.name, 'details': self.__postgres_details})
                self.__postgres_details_changed = False

    def _update_device_info(self):
        logger.info(f"Storing device-info...")
        if device_info:
            logger.debug(f"Data: {device_info}")
            query_device_info = f'INSERT INTO {self.__device_info_table_name} ' \
                                f'(global_uuid , client_id, client_name, site_id, site_name, device_id, device_name, ' \
                                f'site_address, site_city, site_state, site_zip, site_country, site_lat, site_lon, ' \
                                f'time_zone, ' \
                                f'created_on, updated_on) ' \
                                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
                                f'ON CONFLICT (global_uuid) DO UPDATE SET ' \
                                f'client_id = excluded.client_id,' \
                                f'client_name = excluded.client_name,' \
                                f'site_id = excluded.site_id,' \
                                f'site_name = excluded.site_name,' \
                                f'device_id = excluded.device_id,' \
                                f'device_name = excluded.device_name,' \
                                f'site_address = excluded.site_address,' \
                                f'site_city = excluded.site_city,' \
                                f'site_state = excluded.site_state,' \
                                f'site_zip = excluded.site_zip,' \
                                f'site_country = excluded.site_country,' \
                                f'site_lat = excluded.site_lat,' \
                                f'site_lon = excluded.site_lon,' \
                                f'time_zone = excluded.time_zone,' \
                                f'created_on = excluded.created_on,' \
                                f'updated_on = excluded.updated_on'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        device_info_dict: tuple = (device_info.global_uuid,
                                                   device_info.client_id, device_info.client_name,
                                                   device_info.site_id, device_info.site_name,
                                                   device_info.device_id, device_info.device_name,
                                                   device_info.site_address, device_info.site_city,
                                                   device_info.site_state, device_info.site_zip,
                                                   device_info.site_country, device_info.site_lat,
                                                   device_info.site_lon, device_info.time_zone,
                                                   device_info.created_on,
                                                   device_info.updated_on)
                        curs.execute(query_device_info, device_info_dict)

                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated 1 rows on {self.__device_info_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__device_info_table_name}")

    def _update_networks(self):
        logger.info(f"Storing networks_list...")
        networks_list: List[tuple] = []
        for network in NetworkModel.find_all():
            networks_list.append((network.uuid, network.name, network.enable, network.fault, network.history_enable,
                                  Drivers.GENERIC.name, network.created_on, network.updated_on,
                                  device_info.global_uuid))
        if len(networks_list):
            logger.debug(f"Data: {networks_list}")
            query_network = f'INSERT INTO {self.__networks_table_name} ' \
                            f'(uuid, name, enable, fault, history_enable, driver, created_on, updated_on, ' \
                            f'wires_plat_global_uuid) ' \
                            f'VALUES %s ON CONFLICT (uuid) ' \
                            f'DO UPDATE SET ' \
                            f'name = excluded.name, ' \
                            f'enable = excluded.enable, ' \
                            f'fault = excluded.fault, ' \
                            f'history_enable = excluded.history_enable, ' \
                            f'driver = excluded.driver, ' \
                            f'created_on = excluded.created_on, ' \
                            f'updated_on = excluded.updated_on, ' \
                            f'wires_plat_global_uuid = excluded.wires_plat_global_uuid'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_network, networks_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(networks_list)} rows on {self.__networks_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__networks_table_name}")

    def _update_devices(self):
        logger.info(f"Storing devices_list...")
        devices_list: List[tuple] = []
        for device in DeviceModel.find_all():
            devices_list.append((device.uuid, device.network_uuid, device.name, device.enable, device.fault,
                                 device.history_enable, Drivers.GENERIC.name, device.created_on, device.updated_on))
        if len(devices_list):
            logger.debug(f"Data: {devices_list}")
            query_network = f'INSERT INTO {self.__devices_table_name} ' \
                            f'(uuid, network_uuid, name, enable, fault, history_enable, driver, created_on, ' \
                            f'updated_on) ' \
                            f'VALUES %s ON CONFLICT (uuid) ' \
                            f'DO UPDATE SET ' \
                            f'network_uuid = excluded.network_uuid, ' \
                            f'name = excluded.name, ' \
                            f'enable = excluded.enable, ' \
                            f'fault = excluded.fault, ' \
                            f'history_enable = excluded.history_enable, ' \
                            f'driver = excluded.driver, ' \
                            f'created_on = excluded.created_on, ' \
                            f'updated_on = excluded.updated_on'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_network, devices_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(devices_list)} rows on {self.__devices_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__devices_table_name}")

    def _update_networks_tags(self):
        logger.info(f"Storing network_tags_list...")
        network_tags_list: List[tuple] = []
        for network in NetworkModel.find_all():
            if network.tags:
                network_tags: dict = json.loads(network.tags)
                # insert tags from network object
                for network_tag in network_tags.keys():
                    network_tags_list.append((network.uuid, network_tag, network_tags[network_tag]))
        if len(network_tags_list):
            logger.debug(f"Data: {network_tags_list}")
            query_network_tag = f'INSERT INTO {self.__networks_tags_table_name} ' \
                                f'(network_uuid, tag_name, tag_value) ' \
                                f'VALUES %s ON CONFLICT (network_uuid, tag_name) ' \
                                f'DO UPDATE SET tag_value = excluded.tag_value'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        if len(network_tags_list):
                            # Remove comma (,) from ('<uuid>',)
                            in_uuid: str = rreplace(str(tuple(i[0] for i in network_tags_list)), ",)", ")", 1)
                            in_tags_list: str = rreplace(
                                str(tuple((i[0], i[1]) for i in network_tags_list)), ",)", ")", 1)
                            query_delete_network_tag = f'DELETE FROM {self.__networks_tags_table_name} ' \
                                                       f'WHERE network_uuid IN {in_uuid} ' \
                                                       f'AND (network_uuid, tag_name) NOT IN {in_tags_list}'
                            curs.execute(query_delete_network_tag)
                        execute_values(curs, query_network_tag, network_tags_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(network_tags_list)} rows on {self.__networks_tags_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__networks_tags_table_name}")

    def _update_devices_tags(self):
        logger.info(f"Storing device_tags_list...")
        device_tags_list: List[tuple] = []
        for device in DeviceModel.find_all():
            if device.tags:
                device_tags: dict = json.loads(device.tags)
                # insert tags from device object
                for device_tag in device_tags.keys():
                    device_tags_list.append((device.uuid, device_tag, device_tags[device_tag]))
        if len(device_tags_list):
            logger.debug(f"Data: {device_tags_list}")
            query_device_tag = f'INSERT INTO {self.__devices_tags_table_name} ' \
                               f'(device_uuid, tag_name, tag_value) ' \
                               f'VALUES %s ON CONFLICT (device_uuid, tag_name) ' \
                               f'DO UPDATE SET tag_value = excluded.tag_value'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        if len(device_tags_list):
                            # Remove comma (,) from ('<uuid>',)
                            in_uuid: str = rreplace(str(tuple(i[0] for i in device_tags_list)), ",)", ")", 1)
                            in_tags_list: str = rreplace(
                                str(tuple((i[0], i[1]) for i in device_tags_list)), ",)", ")", 1)
                            query_delete_device_tag = f'DELETE FROM {self.__devices_tags_table_name} ' \
                                                      f'WHERE device_uuid IN {in_uuid} ' \
                                                      f'AND (device_uuid, tag_name) NOT IN {in_tags_list}'
                            curs.execute(query_delete_device_tag)
                        execute_values(curs, query_device_tag, device_tags_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(device_tags_list)} rows on {self.__devices_tags_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__devices_tags_table_name}")

    def _update_points_list(self, points_list):
        logger.info(f"Storing point_list...")
        if len(points_list):
            logger.debug(f"Data: {points_list}")
            query_point = f'INSERT INTO {self.__points_table_name} ' \
                          f'(device_uuid, uuid, name, driver) ' \
                          f'VALUES %s ON CONFLICT (uuid) ' \
                          f'DO UPDATE SET ' \
                          f'device_uuid = excluded.device_uuid, ' \
                          f'driver = excluded.driver,' \
                          f'name = excluded.name'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_point, points_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(points_list)} rows on {self.__points_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__points_table_name}")

    def _update_points_values(self, points_values_list):
        logger.info(f"Storing point_value_data_list...")
        if len(points_values_list):
            logger.debug(f"Data: {points_values_list}")
            query_point_value_data = f'INSERT INTO {self.__points_values_table_name} ' \
                                     f'(id, point_uuid, value, value_original, value_raw, fault, fault_message, ' \
                                     f'ts_value, ts_fault) ' \
                                     f'VALUES %s ON CONFLICT (id, point_uuid) DO NOTHING'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        execute_values(curs, query_point_value_data, points_values_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored {len(list(set(points_values_list)))} rows on {self.__points_values_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__points_values_table_name}, no new records")

    def _update_points_tags(self, points_tags_list):
        logger.info(f"Storing point_tag_list...")
        if len(points_tags_list):
            logger.debug(f"Data: {points_tags_list}")
            query_point_tag = f'INSERT INTO {self.__points_tags_table_name} ' \
                              f'(point_uuid, tag_name, tag_value) ' \
                              f'VALUES %s ON CONFLICT (point_uuid, tag_name) ' \
                              f'DO UPDATE SET tag_value = excluded.tag_value'
            with self.__client:
                with self.__client.cursor() as curs:
                    try:
                        if len(points_tags_list):
                            # Remove comma (,) from ('<uuid>',)
                            in_point_uuid: str = rreplace(str(tuple(i[0] for i in points_tags_list)), ",)", ")", 1)
                            in_point_tags_list: str = rreplace(
                                str(tuple((i[0], i[1]) for i in points_tags_list)), ",)", ")", 1)
                            query_delete_point_tag = f'DELETE FROM {self.__points_tags_table_name} ' \
                                                     f'WHERE point_uuid IN {in_point_uuid} ' \
                                                     f'AND (point_uuid, tag_name) NOT IN {in_point_tags_list}'
                            curs.execute(query_delete_point_tag)
                        execute_values(curs, query_point_tag, points_tags_list, page_size=PAGE_SIZE)
                    except psycopg2.Error as e:
                        logger.error(str(e))
            logger.info(f'Stored/updated {len(points_tags_list)} rows on {self.__points_tags_table_name} table')
        else:
            logger.info(f"Nothing to store on {self.__points_tags_table_name}")

    def _create_table_if_not_exists(self):
        query_device_info = f'CREATE TABLE IF NOT EXISTS {self.__device_info_table_name} ' \
                            f'(global_uuid VARCHAR PRIMARY KEY,' \
                            f'client_id VARCHAR,' \
                            f'client_name VARCHAR,' \
                            f'site_id VARCHAR,' \
                            f'site_name VARCHAR,' \
                            f'device_id VARCHAR,' \
                            f'device_name VARCHAR,' \
                            f'site_address VARCHAR,' \
                            f'site_city VARCHAR,' \
                            f'site_state VARCHAR,' \
                            f'site_zip VARCHAR,' \
                            f'site_country VARCHAR,' \
                            f'site_lat VARCHAR,' \
                            f'site_lon VARCHAR,' \
                            f'time_zone VARCHAR,' \
                            f'created_on TIMESTAMP,' \
                            f'updated_on TIMESTAMP);'
        query_network = f'CREATE TABLE IF NOT EXISTS {self.__networks_table_name} ' \
                        f'(uuid VARCHAR PRIMARY KEY,' \
                        f'name VARCHAR,' \
                        f'enable BOOLEAN,' \
                        f'fault BOOLEAN,' \
                        f'history_enable BOOLEAN,' \
                        f'driver VARCHAR,' \
                        f'created_on TIMESTAMP,' \
                        f'updated_on TIMESTAMP,' \
                        f'wires_plat_global_uuid VARCHAR,' \
                        f'CONSTRAINT fk_{self.__device_info_table_name} FOREIGN KEY(wires_plat_global_uuid) ' \
                        f'REFERENCES {self.__device_info_table_name}(global_uuid) ON DELETE RESTRICT);'
        query_network_tag = f'CREATE TABLE IF NOT EXISTS {self.__networks_tags_table_name} ' \
                            f'(network_uuid VARCHAR REFERENCES {self.__networks_table_name} ON DELETE RESTRICT, ' \
                            f'tag_name VARCHAR, ' \
                            f'tag_value VARCHAR,' \
                            f'PRIMARY KEY (network_uuid, tag_name));'
        query_device = f'CREATE TABLE IF NOT EXISTS {self.__devices_table_name} ' \
                       f'(uuid VARCHAR PRIMARY KEY,' \
                       f'network_uuid VARCHAR,' \
                       f'name VARCHAR,' \
                       f'enable BOOLEAN,' \
                       f'fault BOOLEAN,' \
                       f'history_enable BOOLEAN,' \
                       f'driver VARCHAR,' \
                       f'created_on TIMESTAMP,' \
                       f'updated_on TIMESTAMP,' \
                       f'CONSTRAINT fk_{self.__networks_table_name} FOREIGN KEY(network_uuid) ' \
                       f'REFERENCES {self.__networks_table_name}(uuid) ON DELETE RESTRICT);'
        query_device_tag = f'CREATE TABLE IF NOT EXISTS {self.__devices_tags_table_name} ' \
                           f'(device_uuid VARCHAR REFERENCES {self.__devices_table_name} ON DELETE RESTRICT, ' \
                           f'tag_name VARCHAR, ' \
                           f'tag_value VARCHAR,' \
                           f'PRIMARY KEY (device_uuid, tag_name));'
        query_point = f'CREATE TABLE IF NOT EXISTS {self.__points_table_name} ' \
                      f'(device_uuid VARCHAR(80), ' \
                      f'uuid VARCHAR PRIMARY KEY,' \
                      f'name VARCHAR,' \
                      f'driver VARCHAR(80),' \
                      f'CONSTRAINT fk_{self.__devices_table_name} FOREIGN KEY(device_uuid) ' \
                      f'REFERENCES {self.__devices_table_name}(uuid) ON DELETE RESTRICT);'
        query_point_value_data = f'CREATE TABLE IF NOT EXISTS {self.__points_values_table_name} ' \
                                 f'(id INTEGER, ' \
                                 f'point_uuid VARCHAR, ' \
                                 f'value NUMERIC,' \
                                 f'value_original NUMERIC, ' \
                                 f'value_raw VARCHAR, ' \
                                 f'fault BOOLEAN, ' \
                                 f'fault_message VARCHAR,' \
                                 f'ts_value  TIMESTAMP, ' \
                                 f'ts_fault TIMESTAMP,' \
                                 f'CONSTRAINT fk_{self.__points_table_name} FOREIGN KEY(point_uuid) ' \
                                 f'REFERENCES {self.__points_table_name}(uuid) ON DELETE RESTRICT, ' \
                                 f'PRIMARY KEY (id, point_uuid))'
        query_point_tag = f'CREATE TABLE IF NOT EXISTS {self.__points_tags_table_name} ' \
                          f'(point_uuid VARCHAR REFERENCES {self.__points_table_name} ON DELETE RESTRICT, ' \
                          f'tag_name VARCHAR, ' \
                          f'tag_value VARCHAR,' \
                          f'PRIMARY KEY (point_uuid, tag_name));'
        with self.__client:
            with self.__client.cursor() as curs:
                try:
                    curs.execute(query_device_info)
                    curs.execute(query_network)
                    curs.execute(query_network_tag)
                    curs.execute(query_device)
                    curs.execute(query_device_tag)
                    curs.execute(query_point)
                    curs.execute(query_point_value_data)
                    curs.execute(query_point_tag)
                except psycopg2.Error as e:
                    logger.error(str(e))

    def _get_point_last_sync_id(self, point_uuid) -> Union[int, None]:
        if not self.__postgres_details_changed:
            return HistorySyncLogModel.find_last_sync_id_by_type_point_uuid(HistorySyncType.POSTGRES.name, point_uuid)
        """
        This function will return point_last_sync_id and if connection is already closed then we try to reconnect too
        """
        query = f"SELECT MAX(id) FROM {self.__points_values_table_name} WHERE point_uuid=%s;"
        try:
            with self.__client:
                with self.__client.cursor() as curs:
                    curs.execute(query, (point_uuid,))
                    last_sync_id = curs.fetchone()[0]
                    if last_sync_id:
                        return last_sync_id
        except Exception as e:
            logger.error(f'Error: {e}')
            return None
        return 0
