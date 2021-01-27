from ast import literal_eval

from sqlalchemy import and_, or_

from src import db
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
        return PointStoreModel(point_uuid=point_uuid, value_original=None, value=None, value_raw="")

    def raw_value(self) -> any:
        """Parse value from value_raw"""
        if self.value_raw:
            value_raw = literal_eval(self.value_raw)
            return value_raw
        else:
            return None

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
        return bool(res.rowcount)
