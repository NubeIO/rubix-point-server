from threading import Thread

from src.ini_config import config
from src.services.histories.history_local import HistoryLocal
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
from src.services.mqtt_client.mqtt_client import MqttClient
from src.source_drivers.modbus.services.rtu_polling import RtuPolling
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.source_drivers.modbus.services.tcp_polling import TcpPolling
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry


class Background:
    @staticmethod
    def run():
        print("Running Background Task...")
        if config.getboolean('settings', 'enable_mqtt', fallback=False):
            mqtt_thread = Thread(target=MqttClient.get_instance().start, daemon=True)
            mqtt_thread.start()

        if config.getboolean('settings', 'enable_tcp', fallback=False):
            TcpRegistry.get_instance().register()
            tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling, daemon=True)
            tcp_polling_thread.start()

        if config.getboolean('settings', 'enable_rtu', fallback=False):
            RtuRegistry.get_instance().register()
            rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling, daemon=True)
            rtu_polling_thread.start()

        if config.getboolean('settings', 'enable_histories', fallback=False):
            histories_thread = Thread(target=HistoryLocal.get_instance().sync_interval, daemon=True)
            histories_thread.start()

        if config.getboolean('settings', 'enable_cleaner', fallback=False):
            point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register, daemon=True)
            point_cleaner_thread.start()
