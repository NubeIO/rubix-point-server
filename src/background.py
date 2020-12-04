import logging
from threading import Thread

from src.ini_config import *
from src.services.histories.history_local import HistoryLocal
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
from src.services.histories.sync.influxdb import InfluxDB
from src.services.mqtt_client.mqtt_client import create_mqtt_client
from src.source_drivers.modbus.services.rtu_polling import RtuPolling
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.source_drivers.modbus.services.tcp_polling import TcpPolling
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry

logger = logging.getLogger(__name__)


class Background:
    __mqtt_clients = []

    @staticmethod
    def get_mqtt_client():
        return Background.__mqtt_clients

    @staticmethod
    def run():
        logger.info("Running Background Task...")
        if settings__enable_mqtt:
            mqtt_client_list = filter(lambda section: 'mqtt_' in section, config.sections())
            Background.__mqtt_clients = []
            for client_config_title in mqtt_client_list:
                mqtt_client = create_mqtt_client(client_config_title)
                mqtt_thread = Thread(target=mqtt_client.start, daemon=True)
                mqtt_thread.start()
                Background.__mqtt_clients.append(mqtt_client)

        if settings__enable_tcp:
            TcpRegistry.get_instance().register()
            tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling, daemon=True)
            tcp_polling_thread.start()

        if settings__enable_rtu:
            RtuRegistry.get_instance().register()
            rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling, daemon=True)
            rtu_polling_thread.start()

        if settings__enable_histories:
            histories_thread = Thread(target=HistoryLocal.get_instance().sync_interval, daemon=True)
            histories_thread.start()

        if settings__enable_cleaner:
            point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register, daemon=True)
            point_cleaner_thread.start()

        if settings__enable_history_sync:
            history_sync_thread = Thread(target=InfluxDB.get_instance().register)
            history_sync_thread.start()
