from flask import current_app
from sqlalchemy import and_

from src import db
from src.models.point.model_point_store import PointStoreModelMixin, PointStoreModel
from src.utils.model_utils import ModelUtils


class PointStoreHistoryModel(PointStoreModelMixin):
    __tablename__ = 'point_stores_history'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), nullable=False)

    def __repr__(self):
        return f"PointStoreHistory(point_uuid = {self.point_uuid})"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_point_uuid(cls, point_uuid: str):
        return cls.query.filter_by(point_uuid=point_uuid).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        db.session.add(self)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_after(cls, _id: int, point_uuid: str):
        return cls.query.filter(and_(cls.id > _id, cls.point_uuid == point_uuid)).all()

    @classmethod
    def get_latest(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).order_by(cls.__table__.c.ts_value.desc()).first()

    @staticmethod
    def create_history(point_store: PointStoreModel):
        from src import AppSetting
        setting: AppSetting = current_app.config[AppSetting.KEY]
        if setting.services.histories:
            data = ModelUtils.row2dict_default(point_store)
            _point_store_history = PointStoreHistoryModel(**data)
            _point_store_history.save_to_db_no_commit()
