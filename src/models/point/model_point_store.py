from ast import literal_eval

from sqlalchemy import and_, or_

from src import db
from src.interfaces.point import MathOperation
from src.models.device.model_device import DeviceModel
from src.models.network.model_network import NetworkModel
from src.event_dispatcher import EventDispatcher
from src.services.event_service_base import Event, EventType


class PointStoreModel(db.Model):
    __tablename__ = 'point_stores'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)
    value = db.Column(db.Float(), nullable=True)
    value_original = db.Column(db.Float(), nullable=True)
    value_raw = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid: str):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid: str):
        return PointStoreModel(point_uuid=point_uuid, value_original=None, value=None, value_raw="")

    def raw_value(self) -> any:
        """Parse value from value_raw"""
        if self.value_raw:
            value_raw = literal_eval(self.value_raw)
            return value_raw
        else:
            return None

    @classmethod
    def apply_offset(cls, original_value: float, value_offset: float, value_operation: MathOperation) -> float:
        """Do calculations on original value with the help of point details"""
        if original_value is None or value_operation is None:
            return original_value
        value = original_value
        if value_operation == MathOperation.ADD:
            value += value_offset
        elif value_operation == MathOperation.SUBTRACT:
            value -= value_offset
        elif value_operation == MathOperation.MULTIPLY:
            value *= value_offset
        elif value_operation == MathOperation.DIVIDE:
            value /= value_offset
        elif value_operation == MathOperation.BOOL_INVERT:
            value = not bool(value)
        return value

    @classmethod
    def apply_scale(cls, value: float, input_min: float, input_max: float, output_min: float, output_max: float) \
            -> float:
        if value is None or input_min is None or input_max is None or output_min is None or output_max is None:
            return value
        value = ((value - input_min) * (output_max - output_min)) / (input_max - input_min) + output_min
        return value

    def update(self, point, cov_threshold: float = None) -> bool:
        if not self.fault:
            if cov_threshold is None:
                cov_threshold = point.cov_threshold

            value = self.value_original
            if value is not None:
                value = PointStoreModel.apply_scale(value, point.input_min, point.input_max, point.scale_min,
                                                    point.scale_max)
                value = PointStoreModel.apply_offset(value, point.value_offset, point.value_operation)
                value = round(value, point.value_round)

            self.value = value
            self.fault = bool(self.fault)
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(value=self.value,
                            value_original=self.value_original,
                            value_raw=self.value_raw,
                            fault=False,
                            fault_message=None)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.value == None,
                                    db.func.abs(self.__table__.c.value - self.value) >= cov_threshold,
                                    self.__table__.c.fault != self.fault))))
        else:
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(fault=self.fault, fault_message=self.fault_message)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.fault != self.fault,
                                    self.__table__.c.fault_message != self.fault_message,
                                    self.__table__.c.fault != self.fault))))
        db.session.commit()
        return bool(res.rowcount)

    def publish_cov(self, point, device: DeviceModel = None, network: NetworkModel = None,
                    service_name: str = None):
        if point is None:
            raise Exception('point cannot be None when publishing COV')
        if device is None:
            device = DeviceModel.find_by_uuid(point.device_uuid)
        if network is None:
            network = NetworkModel.find_by_uuid(device.network_uuid)
        if device is None or network is None:
            raise Exception(f'Cannot find network or device for point {self.point_uuid}')
        if service_name is None:
            service_name = network.driver

        EventDispatcher.dispatch_from_source(None, Event(EventType.POINT_COV, {
            'point': point,
            'point_store': self,
            'device': device,
            'network': network,
            'source_driver': service_name
        }))
