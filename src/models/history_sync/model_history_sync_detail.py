from sqlalchemy import UniqueConstraint

from src import db
from src.enums.history_sync import HistorySyncType
from src.models.model_base import ModelBase


class HistorySyncDetailModel(ModelBase):
    __tablename__ = 'history_sync_details'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(HistorySyncType), nullable=False, default=HistorySyncType.POSTGRES)
    details = db.Column(db.String(320), nullable=True)

    __table_args__ = (
        UniqueConstraint('type'),
    )

    def __repr__(self):
        return f"HistorySyncDetailModel(type = {self.type})"

    @classmethod
    def update_history_sync_details(cls, history_sync_detail: dict):
        detail: HistorySyncDetailModel = cls.query.filter_by(type=history_sync_detail.get('type')).first()
        if detail:
            detail.update(**history_sync_detail)
        else:
            detail = HistorySyncDetailModel(**history_sync_detail)
            detail.save_to_db()

    @classmethod
    def find_details_by_type(cls, _type: str) -> str:
        detail: HistorySyncDetailModel = cls.query.filter_by(type=_type).first()
        if detail:
            return detail.details
        return ''
