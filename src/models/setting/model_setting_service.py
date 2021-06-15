import uuid as uuid_
import logging

from src import db, ServiceSetting
from src.models.setting.model_setting_base import SettingBaseModel

logger = logging.getLogger(__name__)


class ServiceSettingModel(SettingBaseModel):
    __tablename__ = 'setting_services'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mqtt = db.Column(db.Boolean(80), nullable=False, default=False)
    histories = db.Column(db.Boolean(), nullable=False, default=False)
    cleaner = db.Column(db.Boolean(80), nullable=False, default=False)
    history_sync_influxdb = db.Column(db.Boolean(80), nullable=False, default=False)
    history_sync_postgres = db.Column(db.Boolean(80), nullable=False, default=False)

    def __repr__(self):
        return f"ServiceSetting(uuid = {self.uuid})"

    @classmethod
    def create_default_if_does_not_exists(cls, config: ServiceSetting):
        service_setting = cls.find_one()
        if not service_setting:
            uuid = str(uuid_.uuid4())
            service_setting = ServiceSettingModel(uuid=uuid,
                                                  mqtt=config.mqtt,
                                                  cleaner=config.cleaner,
                                                  history_sync_influxdb=config.history_sync_influxdb,
                                                  history_sync_postgres=config.history_sync_postgres)
            service_setting.save_to_db()
        return ServiceSetting().reload(service_setting.to_dict())
