from ast import literal_eval
from typing import List

import gevent
from mrb.brige import MqttRestBridge
from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod, Response
from sqlalchemy import and_, or_

from src import db
from src.drivers.enums.drivers import Drivers
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

    def update(self, driver: Drivers, cov_threshold: float = None, sync: bool = True) -> bool:
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
            if driver == Drivers.GENERIC:
                """Generic > Modbus point value"""
                self.__sync_point_value_gp_to_mp_process()
                """Generic > BACnet point value"""
                self.__sync_point_value_gp_to_bp_process()
            elif driver == Drivers.MODBUS:
                """Modbus > Generic | BACnet point value"""
                self.__sync_point_value_mp_to_gbp_process()
        return updated

    def __sync_point_value_gp_to_mp(self, modbus_point_uuid: str):
        api_to_topic_mapper(
            api=f"/api/modbus/points_value/uuid/{modbus_point_uuid}",
            destination_identifier='ps',
            body={"value": self.value},
            http_method=HttpMethod.PATCH)

    def __sync_point_value_gp_to_mp_process(self):
        mapping: MPGBPMapping = MPGBPMapping.find_by_generic_point_uuid(self.point_uuid)
        if mapping:
            gevent.spawn(self.__sync_point_value_gp_to_mp, mapping.modbus_point_uuid)

    def __sync_point_value_gp_to_bp(self):
        response: Response = api_to_topic_mapper(api=f"api/mappings/bp_gp/generic/{self.point_uuid}",
                                                 destination_identifier='bacnet',
                                                 http_method=HttpMethod.GET)
        if not response.error:
            api_to_topic_mapper(api=f"/api/bacnet/points/uuid/{response.content.get('bacnet_point_uuid')}",
                                destination_identifier='bacnet',
                                body={"priority_array_write": {"_16": self.value}},
                                http_method=HttpMethod.PATCH)

    def __sync_point_value_gp_to_bp_process(self):
        gevent.spawn(self.__sync_point_value_gp_to_bp())

    def sync_point_value_with_mapping_mp_to_gbp(self, generic_point_uuid: str, bacnet_point_uuid: str,
                                                gp: bool = True, bp: bool = True):
        if not MqttRestBridge.status():
            return
        if generic_point_uuid and gp:
            api_to_topic_mapper(
                api=f"/api/generic/points_value/uuid/{generic_point_uuid}",
                destination_identifier='ps',
                body={"value": self.value},
                http_method=HttpMethod.PATCH)
        elif bacnet_point_uuid and bp:
            api_to_topic_mapper(
                api=f"/api/bacnet/points/uuid/{bacnet_point_uuid}",
                destination_identifier='bacnet',
                body={"priority_array_write": {"_16": self.value}},
                http_method=HttpMethod.PATCH)

    def __sync_point_value_mp_to_gbp_process(self, gp: bool = True, bp: bool = True):
        mapping: MPGBPMapping = MPGBPMapping.find_by_modbus_point_uuid(self.point_uuid)
        if mapping:
            gevent.spawn(self.sync_point_value_with_mapping_mp_to_gbp,
                         mapping.generic_point_uuid, mapping.bacnet_point_uuid,
                         gp, bp)

    @classmethod
    def sync_points_values_mp_to_gbp_process(cls, gp: bool = True, bp: bool = True):
        if not MqttRestBridge.status():
            return
        mappings: List[MPGBPMapping] = MPGBPMapping.find_all()
        for mapping in mappings:
            point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.modbus_point_uuid)
            if point_store:
                point_store.__sync_point_value_mp_to_gbp_process(gp, bp)
