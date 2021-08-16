import json
import logging
import time
from typing import Union, List

import gevent
from influxdb import InfluxDBClient
from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info

from src import InfluxSetting
from src.enums.driver import Drivers
from src.enums.history_sync import HistorySyncType
from src.handlers.exception import exception_handler
from src.models.history_sync.model_history_sync_detail import HistorySyncDetailModel
from src.models.history_sync.model_history_sync_log import HistorySyncLogModel
from src.models.point.model_point import PointModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.services.histories.history_binding import HistoryBinding
from src.utils import Singleton

logger = logging.getLogger(__name__)


class InfluxDB(HistoryBinding, metaclass=Singleton):

    def __init__(self):
        self.__config = None
        self.__client = None
        self.__device_info: Union[DeviceInfoModel, None] = None
        self.__is_connected = False
        self.__influx_details = ''
        self.__influx_details_changed = False

    @property
    def config(self) -> InfluxSetting:
        return self.__config

    def status(self) -> bool:
        return self.__is_connected

    def disconnect(self):
        self.__is_connected = False

    def setup(self, config: InfluxSetting):
        self.__config = config
        self.__influx_details: str = f'{self.config.host}:{self.config.port}:{self.config.database}:' \
                                     f'{self.config.measurement}'
        self.__influx_details_changed = HistorySyncDetailModel.find_details_by_type(
            HistorySyncType.INFLUX.name) != self.__influx_details
        while not self.status():
            self.connect()
            time.sleep(self.config.attempt_reconnect_secs)

        if self.status():
            logger.info("Registering InfluxDB for sync job")
            while True:
                gevent.sleep(self.config.timer * 60)
                self.sync()
        else:
            logger.error("InfluxDB can't be registered with not working client details")

    def connect(self):
        if self.__client:
            self.__client.close()

        try:
            self.__client = InfluxDBClient(host=self.config.host, port=self.config.port, username=self.config.username,
                                           password=self.config.password, database=self.config.database,
                                           ssl=self.config.ssl, verify_ssl=self.config.verify_ssl,
                                           timeout=self.config.timeout, retries=self.config.retries,
                                           path=self.config.path)
            self.__client.ping()
            self.__is_connected = True
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        logger.info('InfluxDB sync has is been called')
        self.__device_info: Union[DeviceInfoModel, None] = get_device_info()
        if not self.__device_info:
            logger.error('Please add device-info on Rubix Service')
            return
        self._sync()

    def _sync(self):
        store = []
        device_info: dict = {
            'client_id': self.__device_info.client_id,
            'client_name': self.__device_info.client_name,
            'site_id': self.__device_info.site_id,
            'site_name': self.__device_info.site_name,
            'device_id': self.__device_info.device_id,
            'device_name': self.__device_info.device_name
        }
        history_sync_log_list: List[dict] = []
        for point in PointModel.find_all():
            point_last_sync_id: int = self._get_point_last_sync_id(point.uuid)
            point_store_histories = PointStoreHistoryModel.get_all_after(point_last_sync_id, point.uuid)
            for psh in point_store_histories:
                tags = device_info.copy()
                point_store_history: PointStoreHistoryModel = psh
                point: PointModel = point_store_history.point
                if point.tags:
                    point_tags = json.loads(point.tags)
                    for point_tag in point_tags:
                        tags[point_tag] = point_tags[point_tag]

                if point.device.tags:
                    device_tags = json.loads(point.device.tags)
                    for device_tag in device_tags:
                        tags[device_tag] = device_tags[device_tag]

                if point.device.network.tags:
                    network_tags = json.loads(point.device.network.tags)
                    for network_tag in network_tags:
                        tags[network_tag] = network_tags[network_tag]

                tags.update({
                    'rubix_point_uuid': point.uuid,
                    'rubix_point_name': point.name,
                    'rubix_device_uuid': point.device.uuid,
                    'rubix_device_name': point.device.name,
                    'rubix_network_uuid': point.device.network.uuid,
                    'rubix_network_name': point.device.network.name,
                    'rubix_driver': Drivers.GENERIC.name,
                })
                fields = {
                    'id': point_store_history.id,
                    'value': point_store_history.value,
                    'value_original': point_store_history.value_original,
                    'value_raw': point_store_history.value_raw,
                    'fault': point_store_history.fault,
                    'fault_message': point_store_history.fault_message,
                }
                row = {
                    'measurement': self.__config.measurement,
                    'tags': tags,
                    'time': point_store_history.ts_value,
                    'fields': fields
                }
                store.append(row)
            if point_store_histories:
                history_sync_log = {'type': HistorySyncType.INFLUX.name,
                                    'point_uuid': point.uuid,
                                    'last_sync_id': point_store_histories[-1].id}
                history_sync_log_list.append(history_sync_log)
        if len(store):
            logger.debug(f"Storing: {store}")
            try:
                self.__client.write_points(store, batch_size=1000)
                if len(history_sync_log_list):
                    HistorySyncLogModel.update_history_sync_logs(history_sync_log_list)
                    if self.__influx_details_changed:
                        HistorySyncDetailModel.update_history_sync_details(
                            {'type': HistorySyncType.INFLUX.name, 'details': self.__influx_details})
                        self.__influx_details_changed = False
                logger.info(f'Stored {len(store)} rows on {self.config.measurement} measurement')
            except Exception as e:
                logger.error(f"Exception: {str(e)}")
        else:
            logger.info("Nothing to store, no new records")

    def _get_point_last_sync_id(self, point_uuid):
        if not self.__influx_details_changed:
            return HistorySyncLogModel.find_last_sync_id_by_type_point_uuid(HistorySyncType.INFLUX.name, point_uuid)
        query = f"SELECT MAX(id), point_uuid FROM {self.config.measurement} WHERE rubix_point_uuid='{point_uuid}'"
        result_set = self.__client.query(query)
        points = list(result_set.get_points())
        if len(points) == 0:
            last_sync_id = 0
        else:
            last_sync_id = list(result_set.get_points())[0].get('max')
        return last_sync_id
