import logging
import random
import re
from typing import Union

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.enums.driver import Drivers
from src.enums.point import HistoryType, GenericPointType
from src.models.device.model_device import DeviceModel
from src.models.model_base import ModelBase
from src.models.network.model_network import NetworkModel
from src.models.point.model_point_store import PointStoreModel
from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.models.point.priority_array import PriorityArrayModel
from src.utils import dbsession
from src.utils.math_functions import eval_arithmetic_expression
from src.utils.model_utils import validate_json

logger = logging.getLogger(__name__)


class PointModel(ModelBase):
    __tablename__ = 'points'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False, default=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=True)
    history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    history_interval = db.Column(db.Integer, nullable=False, default=15)
    writable = db.Column(db.Boolean, nullable=False, default=True)
    priority_array_write = db.relationship('PriorityArrayModel',
                                           backref='point',
                                           lazy=True,
                                           uselist=False,
                                           cascade="all,delete")
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    value_round = db.Column(db.Integer(), nullable=False, default=2)
    value_operation = db.Column(db.String, nullable=True, default="x + 0")
    input_min = db.Column(db.Float())
    input_max = db.Column(db.Float())
    scale_min = db.Column(db.Float())
    scale_max = db.Column(db.Float())
    tags = db.Column(db.String(320), nullable=True)
    point_store = db.relationship('PointStoreModel', backref='point', lazy=True, uselist=False, cascade="all,delete")
    point_store_history = db.relationship('PointStoreHistoryModel', backref='point', lazy=True, cascade="all,delete")
    history_sync_log = db.relationship('HistorySyncLogModel', backref='hsl', lazy=True, cascade="all,delete")
    fallback_value = db.Column(db.Float(), nullable=True)
    disable_mqtt = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.Enum(GenericPointType), nullable=False, default=GenericPointType.FLOAT)
    unit = db.Column(db.String, nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'device_uuid'),
    )

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    @validates('value_operation')
    def validate_value_operation(self, _, value):
        try:
            if value and value.strip():
                eval_arithmetic_expression(value.lower().replace('x', str(random.randint(1, 9))))
        except Exception:
            raise ValueError("Invalid value_operation, must be a valid arithmetic expression")
        return value

    @classmethod
    def find_by_name(cls, network_name: str, device_name: str, point_name: str):
        results = cls.query.filter_by(name=point_name) \
            .join(DeviceModel).filter_by(name=device_name) \
            .join(NetworkModel).filter_by(name=network_name) \
            .first()
        return results

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db()

    def update_point_value(self, point_store: PointStoreModel, cov_threshold: float = None,
                           priority_array_write_obj: PriorityArrayModel = None) -> bool:
        if not point_store.fault:
            if cov_threshold is None:
                cov_threshold = self.cov_threshold

            value = point_store.value_original
            if value is not None:
                value = self.apply_scale(value, self.input_min, self.input_max, self.scale_min,
                                         self.scale_max)
                value = self.apply_value_operation(value, self.value_operation)
                value = round(value, self.value_round)
            point_store.value = self.apply_point_type(value)
        return point_store.update(cov_threshold, priority_array_write_obj)

    @validates('tags')
    def validate_tags(self, _, value):
        """
        Rules for tags:
        - force all tags to be lower case
        - if there is a gap add an underscore
        - no special characters
        """
        if value is not None:
            try:
                return validate_json(value)
            except ValueError:
                raise ValueError('tags needs to be a valid JSON')
        return value

    @validates('history_interval')
    def validate_history_interval(self, _, value):
        if self.history_type == HistoryType.INTERVAL and value is not None and value < 1:
            raise ValueError("history_interval needs to be at least 1, default is 15 (in minutes)")
        return value

    @validates('input_min')
    def validate_input_min(self, _, value):
        if value is not None and self.input_max is not None and value > self.input_max:
            raise ValueError("input_min cannot be greater than input_max")
        return value

    @validates('input_max')
    def validate_input_max(self, _, value):
        if self.input_min is not None and value is not None and self.input_min > value:
            raise ValueError("input_min cannot be greater than input_max")
        return value

    @validates('scale_min')
    def validate_scale_min(self, _, value):
        if value is not None and self.scale_max is not None and value > self.scale_max:
            raise ValueError("scale_min cannot be greater than scale_max")
        return value

    @validates('scale_max')
    def validate_scale_max(self, _, value):
        if self.scale_min is not None and value is not None and self.scale_min > value:
            raise ValueError("scale_min cannot be greater than scale_max")
        return value

    def update(self, **kwargs) -> bool:
        publish_cov: bool = self.disable_mqtt != kwargs.get('disable_mqtt')
        changed: bool = super().update(**kwargs)
        updated: bool = self.update_point_value(self.point_store, 0)
        if updated or publish_cov:
            self.publish_cov(self.point_store)

        return changed

    def update_point_store(self, value: float, priority: int, priority_array_write: dict):
        priority_array_write_obj, highest_priority_value = self.update_priority_value_without_commit(
            value, priority, priority_array_write)
        point_store = PointStoreModel(point_uuid=self.uuid, value_original=highest_priority_value)
        updated = self.update_point_value(point_store, priority_array_write_obj=priority_array_write_obj)
        if updated:
            self.publish_cov(point_store)

    def update_priority_value_without_commit(self, value: float, priority: int, priority_array_write: dict) -> \
            (Union[PriorityArrayModel, None], Union[float, None]):
        if priority_array_write:
            priority_array: PriorityArrayModel = PriorityArrayModel.find_by_point_uuid(
                self.uuid)
            if priority_array:
                highest_priority_value: float = priority_array.update_with_no_commit(**priority_array_write)
                return priority_array, highest_priority_value
            return None, None
        if not priority:
            priority = 16
        if priority not in range(1, 17):
            raise ValueError('priority should be in range(1, 17)')
        if priority:
            priority_array: PriorityArrayModel = PriorityArrayModel.find_by_point_uuid(self.uuid)
            if priority_array:
                highest_priority_value: float = priority_array.update_with_no_commit(**{f"_{priority}": value})
                return priority_array, highest_priority_value
        return None, None

    @classmethod
    def apply_value_operation(cls, original_value, value_operation: str) -> float or None:
        """Do calculations on original value with the help of point details"""
        if original_value is None or value_operation is None or not value_operation.strip():
            return original_value
        return eval_arithmetic_expression(value_operation.lower().replace('x', str(original_value)))

    @classmethod
    def apply_scale(cls, value: float, input_min: float, input_max: float, output_min: float, output_max: float) \
            -> float or None:
        if value is None or input_min is None or input_max is None or output_min is None or output_max is None:
            return value
        if input_min == input_max or output_min == output_max:
            return value
        scaled = ((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min
        if scaled > max(output_max, output_min):
            return max(output_max, output_min)
        elif scaled < min(output_max, output_min):
            return min(output_max, output_min)
        else:
            return scaled

    def apply_point_type(self, value: float):
        if value is not None:
            if self.type == GenericPointType.STRING:
                value = None
            elif self.type == GenericPointType.INT:
                value = round(value, 0)
            elif self.type == GenericPointType.BOOL:
                value = float(bool(value))
        return value

    def publish_cov(self, point_store: PointStoreModel, device: DeviceModel = None, network: NetworkModel = None,
                    force_clear: bool = False):
        if point_store is None:
            raise Exception('Point.publish_cov point_store cannot be None')
        if device is None:
            device = DeviceModel.find_by_uuid(self.device_uuid)
        if network is None:
            network = NetworkModel.find_by_uuid(device.network_uuid)
        if device is None or network is None:
            raise Exception(f'Cannot find network or device for point {self.uuid}')
        priority = self._get_highest_priority_field()

        if self.history_enable \
                and (self.history_type == HistoryType.COV or self.history_type == HistoryType.COV_AND_INTERVAL) \
                and network.history_enable \
                and device.history_enable:
            PointStoreHistoryModel.create_history(point_store)
            dbsession.commit(db)
        if not self.disable_mqtt:
            from src.services.mqtt_client import MqttClient
            MqttClient.publish_point_cov(
                Drivers.GENERIC.name, network, device, self, point_store, force_clear, priority)

    def _get_highest_priority_field(self):
        for i in range(1, 17):
            value = getattr(self.priority_array_write, f'_{i}', None)
            if value is not None:
                return i
        return 16
