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

    # TODO: Change value array to match different drivers

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    def update(self):
        if not self.fault:
            db.session.execute(PointStoreModel.__table__
                               .update()
                               .values(value=self.value, fault=False, fault_message=None)
                               .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                           self.__table__.c.value != self.value)))
        else:
            db.session.execute(PointStoreModel.__table__
                               .update()
                               .values(fault=self.fault, fault_message=self.fault_message)
                               .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                           or_(self.__table__.c.fault != self.fault,
                                               self.__table__.c.fault_message != self.fault_message))))
