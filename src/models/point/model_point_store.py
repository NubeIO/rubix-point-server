from ast import literal_eval

from sqlalchemy import and_, or_

from src import db
from src.source_drivers.modbus.interfaces.point.points import MathOperation


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
        return PointStoreModel(point_uuid=point_uuid, value=None, value_array="")

    def raw_value(self):
        """Parse value from value_array"""
        if self.value_array:
            values = literal_eval(self.value_array)
            return values[0] if len(values) > 0 else None
        else:
            return None

    @classmethod
    def change_raw_value(cls, raw_value, point):
        """Do calculations on raw_value with the help of point details"""
        if raw_value is None:
            return None
        value = raw_value + point.data_offset
        if point.math_operation == MathOperation.ADD:
            value = point.math_operation_value + value
        elif point.math_operation == MathOperation.SUBTRACT:
            value -= point.math_operation_value
        elif point.math_operation == MathOperation.MULTIPLY:
            value *= point.math_operation_value
        elif point.math_operation == MathOperation.DIVIDE:
            value /= point.math_operation_value
        elif point.math_operation == MathOperation.BOOL_INVERT:
            value = not bool(value)
        value = round(value, point.data_round)
        return value

    def update(self, point) -> bool:
        if not self.fault:
            value = PointStoreModel.change_raw_value(self.value, point)
            self.fault = bool(self.fault)
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(value=value,
                            value_array=self.value_array,
                            fault=False,
                            fault_message=None)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.value == None,
                                    db.func.abs(self.__table__.c.value - value) >= point.cov_threshold,
                                    self.__table__.c.fault != self.fault))))
        else:
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(fault=self.fault, fault_message=self.fault_message)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.fault != self.fault,
                                    self.__table__.c.fault_message != self.fault_message,
                                    self.__table__.c.fault != self.fault))))
        db.session.commit()
        return bool(res.rowcount)
