from threading import Thread

from src.services.histories.history_local import HistoryLocal
from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
from src.services.mqtt_client.mqtt_client import MqttClient
from src.source_drivers.modbus.services.rtu_polling import RtuPolling
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.source_drivers.modbus.services.tcp_polling import TcpPolling
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry

# TMP CONFIGS
enable_mqtt = True
enable_histories = True
enable_tcp = False
enable_rtu = True
enable_cleaner = True


class Background:
    @staticmethod
    def run():
        print("Running Background Task...")
        if enable_histories:
            histories_thread = Thread(target=HistoryLocal.get_instance().sync_interval, daemon=True)
            histories_thread.start()

        # if config.getboolean('settings', 'enable_mqtt'):
        if enable_mqtt:
            # mqtt_thread = Thread(target=MqttClient.get_instance().start)
            mqtt_thread = Thread(target=MqttClient.get_instance().start, args=('localhost', 1883), daemon=True)
            mqtt_thread.start()

        if enable_tcp:
            TcpRegistry.get_instance().register()
            tcp_polling_thread = Thread(target=TcpPolling.get_instance().polling, daemon=True)
            tcp_polling_thread.start()

        if enable_rtu:
            RtuRegistry.get_instance().register()
            rtu_polling_thread = Thread(target=RtuPolling.get_instance().polling, daemon=True)
            rtu_polling_thread.start()

        if enable_cleaner:
            point_cleaner_thread = Thread(target=PointStoreHistoryCleaner.register, daemon=True)
            point_cleaner_thread.start()
