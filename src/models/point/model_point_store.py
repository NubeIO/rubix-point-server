import json
from ast import literal_eval
from typing import List

import gevent
from flask import Response
from rubix_http.method import HttpMethod
from rubix_http.request import gw_request
from sqlalchemy import and_, or_

from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.enums.mapping.mapping import MapType, MappingState
from src.drivers.modbus.models.mapping import MPGBPMapping
from src.utils.model_utils import get_datetime


class PointStoreModelMixin(db.Model):
    __abstract__ = True
    value = db.Column(db.Float(), nullable=True)
    value_original = db.Column(db.Float(), nullable=True)
    value_raw = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts_value = db.Column(db.DateTime())
    ts_fault = db.Column(db.DateTime())


class PointStoreModel(PointStoreModelMixin):
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

    def update(self, driver: Drivers, cov_threshold: float = None) -> bool:
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
                                    and_(db.func.abs(self.__table__.c.value - self.value) >= cov_threshold,
                                         self.__table__.c.value != self.value),
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
        if updated:
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
        gw_request(
            api=f"/ps/api/modbus/points_value/uuid/{modbus_point_uuid}",
            body={"value": self.value},
            http_method=HttpMethod.PATCH
        )

    def __sync_point_value_gp_to_mp_process(self):
        mapping: MPGBPMapping = MPGBPMapping.find_by_mapped_point_uuid_type(self.point_uuid, MapType.GENERIC)
        if mapping and mapping.mapping_state == MappingState.MAPPED:
            gevent.spawn(self.__sync_point_value_gp_to_mp, mapping.modbus_point_uuid)

    def __sync_point_value_gp_to_bp(self):
        response: Response = gw_request(api=f"/bacnet/api/mappings/bp_gp/generic/{self.point_uuid}")
        if response.status_code == 200:
            gw_request(
                api=f"/bacnet/api/bacnet/points/uuid/{json.loads(response.data).get('bacnet_point_uuid')}",
                body={"priority_array_write": {"_16": self.value}},
                http_method=HttpMethod.PATCH
            )

    def __sync_point_value_gp_to_bp_process(self):
        gevent.spawn(self.__sync_point_value_gp_to_bp)

    def sync_point_value_with_mapping_mp_to_gbp(self, map_type: str, mapped_point_uuid: str,
                                                gp: bool = True, bp: bool = True):
        if map_type in (MapType.GENERIC.name, MapType.GENERIC) and gp:
            gw_request(
                api=f"/ps/api/generic/points_value/uuid/{mapped_point_uuid}",
                body={"value": self.value},
                http_method=HttpMethod.PATCH
            )
        elif map_type in (MapType.BACNET.name, MapType.BACNET) and bp:
            gw_request(
                api=f"/bacnet/api/bacnet/points/uuid/{mapped_point_uuid}",
                body={"priority_array_write": {"_16": self.value}},
                http_method=HttpMethod.PATCH
            )

    def __sync_point_value_mp_to_gbp_process(self, gp: bool = True, bp: bool = True):
        mapping: MPGBPMapping = MPGBPMapping.find_by_point_uuid(self.point_uuid)
        if mapping and mapping.mapping_state == MappingState.MAPPED:
            gevent.spawn(
                self.sync_point_value_with_mapping_mp_to_gbp,
                mapping.type, mapping.mapped_point_uuid,
                gp, bp
            )

    @classmethod
    def sync_points_values_mp_to_gbp_process(cls, gp: bool = True, bp: bool = True):
        mappings: List[MPGBPMapping] = MPGBPMapping.find_all()
        for mapping in mappings:
            if mapping.mapping_state == MappingState.MAPPED:
                point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.point_uuid)
                if point_store:
                    point_store.__sync_point_value_mp_to_gbp_process(gp, bp)
