from sqlalchemy import and_, or_

from src import db


class PointStoreModel(db.Model):
    __tablename__ = 'point_stores'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)
    value = db.Column(db.Float(), nullable=True)
    value_array = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid):
        return PointStoreModel(point_uuid=point_uuid, value=0)

    def update(self) -> bool:
        if not self.fault:
            res = db.session.execute(self.__table__
                                     .update()
                                     .values(value=self.value, value_array=self.value_array,
                                             fault=False, fault_message=None)
                                     .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                                 or_(self.__table__.c.value != self.value,
                                                     self.__table__.c.value_array != self.value_array,
                                                     self.__table__.c.fault != self.fault))))
        else:
            res = db.session.execute(self.__table__
                                     .update()
                                     .values(fault=self.fault, fault_message=self.fault_message)
                                     .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                                 or_(self.__table__.c.fault != self.fault,
                                                     self.__table__.c.fault_message != self.fault_message,
                                                     self.__table__.c.fault != self.fault))))
        return bool(res.rowcount)
