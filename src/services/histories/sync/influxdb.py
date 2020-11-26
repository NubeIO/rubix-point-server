import logging
import time

import schedule
from influxdb import InfluxDBClient

from src.ini_config import config
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.wires.model_wires_plat import WiresPlatModel
from src.services.histories.history_binding import HistoryBinding

logger = logging.getLogger(__name__)


class InfluxDB(HistoryBinding):
    __wires_plat = None
    __is_connected = False

    __instance = None
    __client = None

    def __init__(self):
        if InfluxDB.__instance:
            raise Exception("InfluxDB class is a singleton class!")
        else:
            self.host = config.get('influx_db', 'host', fallback='localhost')
            self.port = config.get('influx_db', 'port', fallback=8086)
            self.database = config.get('influx_db', 'database', fallback='db')
            self.username = config.get('influx_db', 'username', fallback='')
            self.password = config.get('influx_db', 'password', fallback='')
            self.verify_ssl = config.getboolean('influx_db', 'verify_ssl', fallback=False)
            self.timeout = config.getint('influx_db', 'timeout', fallback=None)
            self.retries = config.getint('influx_db', 'retries', fallback=3)
            self.path = config.get('influx_db', 'path', fallback=None)
            self.measurement = config.get('influx_db', 'measurement', fallback='history')
            self.push_period_minutes = config.getint('influx_db', 'timer', fallback=1)
            InfluxDB.__instance = self
            InfluxDB.__instance.connect()

    @staticmethod
    def get_instance():
        if InfluxDB.__instance is None:
            InfluxDB()
        return InfluxDB.__instance

    def status(self) -> bool:
        return InfluxDB.__is_connected

    def exception_handling_decorator(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
                InfluxDB.__is_connected = True
            except Exception as e:
                InfluxDB.__is_connected = False
                logger.error(f'Syncing Error: {str(e)}')

        return inner

    def register(self):
        if InfluxDB.__is_connected:
            logger.info("Registering InfluxDB for scheduler job")
            # schedule.every(5).seconds.do(self.sync)  # for testing
            schedule.every(self.push_period_minutes).minutes.do(self.sync)
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            logger.error("InfluxDB can't be registered with not working client details")

    def connect(self):
        if InfluxDB.__client:
            InfluxDB.__client.close()

        try:
            InfluxDB.__client = InfluxDBClient(host=self.host,
                                               port=self.port,
                                               username=self.username,
                                               password=self.password,
                                               database=self.database,
                                               verify_ssl=self.verify_ssl,
                                               timeout=self.timeout,
                                               retries=self.retries,
                                               path=self.path)
            InfluxDB.__client.ping()
            InfluxDB.__is_connected = True
        except Exception as e:
            InfluxDB.__is_connected = False
            logger.error(f'Connection Error: {str(e)}')

    @exception_handling_decorator
    def sync(self):
        logger.info('InfluxDB sync has is been called')
        InfluxDB.__wires_plat = WiresPlatModel.find_one()
        if not InfluxDB.__wires_plat:
            logger.error("Please add wires-plat")
        else:
            self._sync()

    def _sync(self):
        store = []
        plat = {
            'client_id': InfluxDB.__wires_plat.client_id,
            'site_id': InfluxDB.__wires_plat.site_id,
            'device_id': InfluxDB.__wires_plat.device_id
        }
        for point_store_history in PointStoreHistoryModel.get_all_after(self._get_last_sync_id()):
            tags = plat.copy()
            tags.update({
                'point_uuid': point_store_history.point.uuid,
                'name': point_store_history.point.name,
                'reg': point_store_history.point.reg,
                'type': point_store_history.point.type,
            })
            fields = {
                'id': point_store_history.id,
                'val': point_store_history.value,
                'value_array': point_store_history.value_array,
                'fault': point_store_history.fault,
                'fault_message': point_store_history.fault_message,
            }
            row = {
                'measurement': 'history',
                'tags': tags,
                'time': point_store_history.ts,
                'fields': fields
            }
            store.append(row)
        if len(store):
            logger.debug(f"Storing: {store}")
            InfluxDB.__client.write_points(store)
            logger.info(f'Stored {len(store)} rows on {self.measurement} measurement')

    def _get_last_sync_id(self):
        query = f'SELECT MAX(id) FROM {self.measurement}'
        result_set = InfluxDB.__client.query(query)
        points = list(result_set.get_points())
        if len(points) == 0:
            last_sync_id = 0
        else:
            last_sync_id = list(result_set.get_points())[0].get('max')
        return last_sync_id
