import uuid as uuid_
import logging

from src import db, DriverSetting
from src.models.setting.model_setting_base import SettingBaseModel

logger = logging.getLogger(__name__)


class DriverSettingModel(SettingBaseModel):
    __tablename__ = 'setting_drivers'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    generic = db.Column(db.Boolean(80), nullable=False, default=False)
    modbus_rtu = db.Column(db.Boolean(), nullable=False, default=False)
    modbus_tcp = db.Column(db.Boolean(80), nullable=False, default=False)

    def __repr__(self):
        return f"DriverSetting(uuid = {self.uuid})"

    @classmethod
    def create_default_if_does_not_exists(cls, config: DriverSetting):
        driver_setting = cls.find_one()
        if not driver_setting:
            uuid = str(uuid_.uuid4())
            driver_setting = DriverSettingModel(uuid=uuid,
                                                generic=config.generic,
                                                modbus_rtu=config.modbus_rtu,
                                                modbus_tcp=config.modbus_tcp)
            driver_setting.save_to_db()
        return DriverSetting().reload(driver_setting.to_dict())
