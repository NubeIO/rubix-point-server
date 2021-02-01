import json
import logging
import time

import schedule
from influxdb import InfluxDBClient

from src import InfluxSetting
from src.handlers.exception import exception_handler
from src.models.point.model_point import PointModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.wires.model_wires_plat import WiresPlatModel
from src.services.histories.history_binding import HistoryBinding
from src.utils import Singleton

logger = logging.getLogger(__name__)


class InfluxDB(HistoryBinding, metaclass=Singleton):

    def __init__(self):
        self.__config = None
        self.__client = None
        self.__wires_plat = None
        self.__is_connected = False

    @property
    def config(self) -> InfluxSetting:
        return self.__config

    def status(self) -> bool:
        return self.__is_connected

    def disconnect(self):
        self.__is_connected = False

    def setup(self, config: InfluxSetting):
        self.__config = config
        while not self.status():
            self.connect()
            time.sleep(self.config.attempt_reconnect_secs)

        if self.status():
            logger.info("Registering InfluxDB for scheduler job")
            # schedule.every(5).seconds.do(self.sync)  # for testing
            schedule.every(self.config.timer).minutes.do(self.sync)
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            logger.error("InfluxDB can't be registered with not working client details")

    def connect(self):
        if self.__client:
            self.__client.close()

        try:
            self.__client = InfluxDBClient(host=self.config.host, port=self.config.port, username=self.config.username,
                                           password=self.config.password, database=self.config.database,
                                           verify_ssl=self.config.verify_ssl, timeout=self.config.timeout,
                                           retries=self.config.retries, path=self.config.path)
            self.__client.ping()
            self.__is_connected = True
        except Exception as e:
            self.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handler
    def sync(self):
        logger.info('InfluxDB sync has is been called')
        self.__wires_plat = WiresPlatModel.find_one()
        if not self.__wires_plat:
            logger.error("Please add wires-plat")
        else:
            self._sync()

    def _sync(self):
        store = []
        plat = {
            'client_id': self.__wires_plat.client_id,
            'site_id': self.__wires_plat.site_id,
            'device_id': self.__wires_plat.device_id
        }
        for psh in PointStoreHistoryModel.get_all_after(self._get_last_sync_id()):
            tags = plat.copy()
            point_store_history: PointStoreHistoryModel = psh
            point: PointModel = point_store_history.point
            point_tags = json.loads(point.tags)
            for point_tag in point_tags:
                tags[point_tag] = point_tags[point_tag]
            tags.update({
                'point_uuid': point.uuid,
                'point_name': point.name,
                'device_name': point.device.name,
                'network_name': point.device.network.name,
                'driver': point.driver,
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
                'measurement': 'history',
                'tags': tags,
                'time': point_store_history.ts_value,
                'fields': fields
            }
            store.append(row)
        if len(store):
            logger.debug(f"Storing: {store}")
            self.__client.write_points(store)
            logger.info(f'Stored {len(store)} rows on {self.config.measurement} measurement')
        else:
            logger.debug("Nothing to store, no new records")

    def _get_last_sync_id(self):
        query = f'SELECT MAX(id) FROM {self.config.measurement}'
        result_set = self.__client.query(query)
        points = list(result_set.get_points())
        if len(points) == 0:
            last_sync_id = 0
        else:
            last_sync_id = list(result_set.get_points())[0].get('max')
        return last_sync_id
