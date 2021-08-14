from typing import List

from sqlalchemy import UniqueConstraint

from src import db
from src.enums.history_sync import HistorySyncType
from src.models.model_base import ModelBase


class HistorySyncLogModel(ModelBase):
    __tablename__ = 'history_sync_logs'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(HistorySyncType), nullable=False, default=HistorySyncType.POSTGRES)
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), nullable=False)
    last_sync_id = db.Column(db.Integer(), nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint('type', 'point_uuid'),
    )

    def __repr__(self):
        return f"HistorySyncLogModel(point_uuid = {self.point_uuid})"

    @classmethod
    def update_history_sync_logs(cls, history_sync_log_list: List[dict]):
        for history_sync_log in history_sync_log_list:
            log: HistorySyncLogModel = cls.query.filter_by(type=history_sync_log.get('type'),
                                                           point_uuid=history_sync_log.get('point_uuid')).first()
            if log:
                log.update(**history_sync_log)
            else:
                log = HistorySyncLogModel(**history_sync_log)
                log.save_to_db()

    @classmethod
    def find_last_sync_id_by_type_point_uuid(cls, _type: str, point_uuid: str) -> int:
        log: HistorySyncLogModel = cls.query.filter_by(type=_type, point_uuid=point_uuid).first()
        if log:
            return log.last_sync_id
        return 0
