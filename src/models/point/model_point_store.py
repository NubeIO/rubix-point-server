import json
from ast import literal_eval

import gevent
from flask import Response
from rubix_http.method import HttpMethod
from rubix_http.request import gw_request
from sqlalchemy import and_, or_

from src import db
from src.enums.mapping import MappingState
from src.models.point.priority_array import PriorityArrayModel
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

    def update(self, driver: Drivers, cov_threshold: float = None,
               priority_array_write_obj: PriorityArrayModel = None) -> bool:
    def update(self, cov_threshold: float = None) -> bool:
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
            if not priority_array_write_obj:
                priority_array_write_obj = PriorityArrayModel.find_by_point_uuid(self.point_uuid)
            priority_array_write: dict = priority_array_write_obj.to_dict() if priority_array_write_obj \
                else {"_16": self.value}
            """Generic > Modbus point value"""
            self.__sync_point_value_gp_to_mp_process(priority_array_write)
            """Generic > BACnet point value"""
            self.__sync_point_value_gp_to_bp_process(priority_array_write)
        return updated

    @staticmethod
    def __sync_point_value_gp_to_mp(modbus_point_uuid: str, priority_array_write: dict):
        priority_array_write.pop('point_uuid', None)
        gw_request(
            api=f"/modbus/api/modbus/points_value/uuid/{modbus_point_uuid}",
            body={"priority_array_write": priority_array_write},
            http_method=HttpMethod.PATCH
        )

    def __sync_point_value_gp_to_mp_process(self, priority_array_write: dict):
        response: Response = gw_request(api=f"/modbus/api/mappings/mp_gbp/generic/{self.point_uuid}")
        if response.status_code == 200:
            mapping = json.loads(response.data)
            if mapping and mapping.get('mapping_state') in (MappingState.MAPPED, MappingState.MAPPED.name):
                gevent.spawn(self.__sync_point_value_gp_to_mp, mapping.get('point_uuid'), priority_array_write)

    @staticmethod
    def __sync_point_value_gp_to_bp(bacnet_point_uuid, priority_array_write: dict):
        priority_array_write.pop('point_uuid', None)
        gw_request(
            api=f"/bacnet/api/bacnet/points/uuid/{bacnet_point_uuid}",
            body={"priority_array_write": priority_array_write},
            http_method=HttpMethod.PATCH
        )

    def __sync_point_value_gp_to_bp_process(self, priority_array_write: dict):
        response: Response = gw_request(api=f"/bacnet/api/mappings/bp_gp/generic/{self.point_uuid}")
        if response.status_code == 200:
            mapping = json.loads(response.data)
            if mapping and mapping.get('mapping_state') in (MappingState.MAPPED, MappingState.MAPPED.name):
                gevent.spawn(self.__sync_point_value_gp_to_bp, mapping.get('point_uuid'), priority_array_write)
