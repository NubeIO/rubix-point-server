import uuid as _uuid

from flask import current_app
from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src import FlaskThread, InfluxSetting, PostgresSetting
from src.models.setting.model_setting_driver import DriverSettingModel
from src.models.setting.model_setting_influx import InfluxSettingModel
from src.models.setting.model_setting_mqtt import MqttSettingModel
from src.models.setting.model_setting_postgres import PostgresSettingModel
from src.models.setting.model_setting_service import ServiceSettingModel
from src.resources.rest_schema.schema_setting import influx_setting_all_attributes, influx_setting_return_attributes, \
    postgres_setting_all_attributes, postgres_setting_return_attributes, mqtt_setting_all_attributes, \
    mqtt_setting_return_attributes, driver_setting_all_attributes, service_setting_all_attributes, \
    driver_setting_return_attributes, service_setting_return_attributes
from src.services.histories.sync.influxdb import InfluxDB
from src.services.histories.sync.postgresql import PostgreSQL
from src.services.mqtt_client import MqttClient
from src.setting import MqttSetting, AppSetting


class DriverSettingResource(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in driver_setting_all_attributes:
        patch_parser.add_argument(attr,
                                  type=driver_setting_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(driver_setting_return_attributes)
    def get(cls):
        return DriverSettingModel.find_one()

    @classmethod
    def patch(cls):
        data = cls.patch_parser.parse_args()
        driver_setting = DriverSettingModel.find_one()
        if not driver_setting:
            raise NotFoundException('Driver setting not found')
        driver_setting.update(**data)
        return {"message": 'Please restart app to apply the changes'}


class ServiceSettingResource(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in service_setting_all_attributes:
        patch_parser.add_argument(attr,
                                  type=service_setting_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(service_setting_return_attributes)
    def get(cls):
        return ServiceSettingModel.find_one()

    @classmethod
    def patch(cls):
        data = cls.patch_parser.parse_args()
        service_setting = ServiceSettingModel.find_one()
        if not service_setting:
            raise NotFoundException('Service setting not found')
        service_setting.update(**data)
        return {'message': 'Please restart app to apply the changes'}


class InfluxSettingResource(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in influx_setting_all_attributes:
        patch_parser.add_argument(attr,
                                  type=influx_setting_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(influx_setting_return_attributes)
    def get(cls):
        return InfluxSettingModel.find_one()

    @classmethod
    def patch(cls):
        data = cls.patch_parser.parse_args()
        influx_setting = InfluxSettingModel.find_one()
        if not influx_setting:
            raise NotFoundException('Influx setting not found')
        update = influx_setting.update(**data)
        if update:
            InfluxDB().restart_influx(InfluxSetting().reload(influx_setting.to_dict()))
        return {'message': 'Successfully restarted influx db'}


class PostgresSettingResource(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in postgres_setting_all_attributes:
        patch_parser.add_argument(attr,
                                  type=postgres_setting_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(postgres_setting_return_attributes)
    def get(cls):
        postgres_setting = PostgresSettingModel.find_one()
        return postgres_setting

    @classmethod
    def patch(cls):
        data = cls.patch_parser.parse_args()
        postgres_setting = PostgresSettingModel.find_one()
        if not postgres_setting:
            raise NotFoundException('Postgres setting not found')
        update = postgres_setting.update(**data)
        if update:
            PostgreSQL().restart_postgres(PostgresSetting().reload(postgres_setting.to_dict()))
        return {'message': 'Successfully restarted postgres db'}


class MqttSettingResource(RubixResource):
    parser = reqparse.RequestParser()
    for attr in mqtt_setting_all_attributes:
        parser.add_argument(attr,
                            type=mqtt_setting_all_attributes[attr]['type'],
                            required=mqtt_setting_all_attributes[attr].get('required', False),
                            help=mqtt_setting_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(mqtt_setting_return_attributes)
    def get(cls):
        mqtt_setting = MqttSettingModel.find_all()
        return mqtt_setting

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        uuid = str(_uuid.uuid4())
        mqtt_setting: MqttSettingModel = MqttSettingModel(uuid=uuid, **data)
        mqtt_setting.save_to_db()
        setting: AppSetting = current_app.config[AppSetting.KEY]
        if setting.services.mqtt and mqtt_setting.enabled:
            mqtt_client = MqttClient()
            FlaskThread(target=mqtt_client.start, daemon=True,
                        kwargs={'config': MqttSetting().reload(mqtt_setting.to_dict())}).start()
            return {'message': 'Successfully started mqtt client'}
        return {'message': 'Successfully added mqtt client'}


class MqttSettingResourceByUUID(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in mqtt_setting_all_attributes:
        patch_parser.add_argument(attr,
                                  type=mqtt_setting_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def patch(cls, uuid):
        data = cls.patch_parser.parse_args()
        mqtt_setting = MqttSettingModel.find_by_uuid(uuid)
        if not mqtt_setting:
            raise NotFoundException('Mqtt setting not found')
        mqtt_setting.update(**data)
        return {'message': 'Please restart app to apply the changes'}

    @classmethod
    def delete(cls, uuid):
        mqtt_setting = MqttSettingModel.find_by_uuid(uuid)
        if mqtt_setting is None:
            raise NotFoundException(f'Does not exist {uuid}')
        mqtt_setting.delete_from_db()
        return {'message': 'Please restart app to apply the changes'}
