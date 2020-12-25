import logging
from threading import Thread

from flask import current_app

from src.ini_config import *
from src.services.histories.history_local import HistoryLocal
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
from src.services.histories.sync.influxdb import InfluxDB
from src.services.mqtt_client.mqtt_client import MqttClient
from src.services.mqtt_client.mqtt_client_base import create_mqtt_client
from src.source_drivers.generic.services.generic_point_listener import GenericPointListener
from src.source_drivers.modbus.services.modbus_polling import RtuPolling, TcpPolling
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry

logger = logging.getLogger(__name__)


class Background:
    __mqtt_clients = []

    @staticmethod
    def get_mqtt_client():
        return Background.__mqtt_clients

    @staticmethod
    def run():
        logger.info("Starting Services...")

        # Services
        if settings__enable_mqtt:
            mqtt_client_list = filter(lambda section: 'mqtt_' in section, config.sections())
            Background.__mqtt_clients = []
            for client_config_title in mqtt_client_list:
                mqtt_client = create_mqtt_client(client_config_title, MqttClient)
                mqtt_thread = Thread(target=mqtt_client.start, daemon=True)
                mqtt_thread.start()
                Background.__mqtt_clients.append(mqtt_client)

        if settings__enable_histories:
            histories_thread = Thread(target=HistoryLocal().sync_interval, daemon=True)
            histories_thread.start()

        if settings__enable_cleaner:
            point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register, daemon=True)
            point_cleaner_thread.start()

        if settings__enable_history_sync:
            history_sync_thread = Thread(target=InfluxDB().register)
            history_sync_thread.start()

        # Drivers
        logger.info("Starting Drivers...")

        if settings__enable_generic:
            generic_listener_thread = Thread(target=GenericPointListener().start, daemon=True)
            generic_listener_thread.start()

        if settings__enable_modbus_tcp:
            TcpRegistry().register()
            tcp_polling_thread = Thread(target=TcpPolling().polling, daemon=True)
            tcp_polling_thread.start()

        if settings__enable_modbus_rtu:
            RtuRegistry().register()
            rtu_polling_thread = Thread(target=RtuPolling().polling, daemon=True)
            rtu_polling_thread.start()
