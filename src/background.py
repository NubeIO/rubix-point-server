import logging
from threading import Thread

from flask import current_app

from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:

    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.KEY]
        logger.info("Starting Services...")

        # Services
        if setting.services.mqtt:
            from src.services.mqtt_client import MqttClient
            for config in setting.mqtt_settings:
                if not config.enabled:
                    continue
                mqtt_client = MqttClient()
                FlaskThread(target=mqtt_client.start, daemon=True, kwargs={'config': config, 'logger': logger}).start()

        if setting.services.histories:
            from src.services.histories.history_local import HistoryLocal
            FlaskThread(target=HistoryLocal().sync_interval, daemon=True).start()

        if setting.services.cleaner:
            from src.services.histories.point_store_history_cleaner import PointStoreHistoryCleaner
            FlaskThread(target=PointStoreHistoryCleaner().setup, daemon=True, kwargs={'logger': logger}).start()

        if setting.services.history_sync:
            from src.services.histories.sync.influxdb import InfluxDB
            FlaskThread(target=InfluxDB().setup, daemon=True,
                        kwargs={'config': setting.influx, 'logger': logger}).start()

        # Drivers
        logger.info("Starting Drivers...")

        if setting.drivers.generic:
            from src.source_drivers.generic.services.generic_point_listener import GenericPointListener
            FlaskThread(target=GenericPointListener().start, daemon=True,
                        kwargs={'config': setting.listener, 'logger': logger}).start()

        if setting.drivers.modbus_tcp:
            from src.source_drivers.modbus.services import TcpPolling, TcpRegistry
            TcpRegistry().register()
            FlaskThread(target=TcpPolling().polling, daemon=True).start()

        if setting.drivers.modbus_rtu:
            from src.source_drivers.modbus.services import RtuPolling, RtuRegistry
            RtuRegistry().register()
            FlaskThread(target=RtuPolling().polling, daemon=True).start()
