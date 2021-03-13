from ast import literal_eval
from typing import List

from mrb.brige import MqttRestBridge
from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod, Response
from sqlalchemy import and_, or_

from src import db, FlaskThread
from src.drivers.modbus.models.mapping import MPGBPMapping
from src.utils.model_utils import get_datetime


class PointStoreModelMixin(object):
    value = db.Column(db.Float(), nullable=True)
    value_original = db.Column(db.Float(), nullable=True)
    value_raw = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts_value = db.Column(db.DateTime())
    ts_fault = db.Column(db.DateTime())


class PointStoreModel(PointStoreModelMixin, db.Model):
    __tablename__ = 'point_stores'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid: str):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid: str):
        return PointStoreModel(point_uuid=point_uuid, value_raw="")

    def raw_value(self) -> any:
        """Parse value from value_raw"""
        if self.value_raw:
            value_raw = literal_eval(self.value_raw)
            return value_raw
        else:
            return None

    def update(self, cov_threshold: float = None, sync: bool = True) -> bool:
        ts = get_datetime()
        if not self.fault:
            self.fault = bool(self.fault)
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(value=self.value,
                            value_original=self.value_original,
                            value_raw=self.value_raw,
                            fault=False,
                            fault_message=None,
                            ts_value=ts)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.value == None,
                                    db.func.abs(self.__table__.c.value - self.value) >= cov_threshold,
                                    self.__table__.c.fault != self.fault))))
            if res.rowcount:  # WARNING: this could cause secondary write to db is store if fetched/linked from DB
                self.ts_value = ts
        else:
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(fault=self.fault,
                            fault_message=self.fault_message,
                            ts_fault=ts)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.fault != self.fault,
                                    self.__table__.c.fault_message != self.fault_message))))
            if res.rowcount:  # WARNING: this could cause secondary write to db is store if fetched/linked from DB
                self.ts_fault = ts
        db.session.commit()
        updated: bool = bool(res.rowcount)
        if MqttRestBridge.status() and updated and sync:
            """Generic Point value is updated, need to sync BACnet Point value"""
            FlaskThread(target=self.__sync_point_value_bp_gp, daemon=True).start()
            """Modbus Point value is updated, need to sync Generic & BACnet Point"""
            FlaskThread(target=self.__sync_point_value_mp_gbp, daemon=True).start()
        return updated

    def __sync_point_value_bp_gp(self):
        response: Response = api_to_topic_mapper(api=f"api/mappings/bp_gp/generic/{self.point_uuid}",
                                                 destination_identifier='bacnet',
                                                 http_method=HttpMethod.GET)
        if not response.error:
            api_to_topic_mapper(api=f"/api/bacnet/points/uuid/{response.content.get('bacnet_point_uuid')}",
                                destination_identifier='bacnet',
                                body={"priority_array_write": {"_16": self.value}},
                                http_method=HttpMethod.PATCH)

    def sync_point_value_with_mapping_mp_gbp(self, mapping: MPGBPMapping, gp: bool = True, bp=True):
        if not MqttRestBridge.status():
            return
        if mapping.generic_point_uuid and gp:
            api_to_topic_mapper(
                api=f"/api/generic/points_value/uuid/{mapping.generic_point_uuid}",
                destination_identifier='ps',
                body={"value": self.value},
                http_method=HttpMethod.PATCH)
        elif mapping.bacnet_point_uuid and bp:
            api_to_topic_mapper(
                api=f"/api/bacnet/points/uuid/{mapping.bacnet_point_uuid}",
                destination_identifier='bacnet',
                body={"priority_array_write": {"_16": self.value}},
                http_method=HttpMethod.PATCH)

    def __sync_point_value_mp_gbp(self, gp: bool = True, bp=True):
        mapping: MPGBPMapping = MPGBPMapping.find_by_modbus_point_uuid(self.point_uuid)
        if mapping:
            self.sync_point_value_with_mapping_mp_gbp(mapping, gp, bp)

    @classmethod
    def sync_points_values_mp_gbp(cls, gp: bool = True, bp=True):
        if not MqttRestBridge.status():
            return
        mappings: List[MPGBPMapping] = MPGBPMapping.find_all()
        for mapping in mappings:
            point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.modbus_point_uuid)
            if point_store:
                FlaskThread(target=point_store.__sync_point_value_mp_gbp, daemon=True,
                            kwargs={'gp': gp, 'bp': bp}).start()
