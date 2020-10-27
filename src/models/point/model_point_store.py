from src import db


class PointStoreModel(db.Model):
    __tablename__ = 'point_stores'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)
    value = db.Column(db.Float(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # TODO: add value array somehow

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    def update_to_db_cov_only(self):
        if self.value is None:
            return
        db.session.query(PointStoreModel).filter(PointStoreModel.point_uuid == self.point_uuid and
                                                 (PointStoreModel.value != self.value or
                                                  PointStoreModel.fault == True)) \
            .update({
                PointStoreModel.value: self.value,
                PointStoreModel.value_array: self.value_array,
                PointStoreModel.fault: False,
                PointStoreModel.fault_message: None,
            })

    def update_with_fault(self):
        db.session.query(PointStoreModel).filter(PointStoreModel.point_uuid == self.point_uuid and
                                                 (PointStoreModel.fault == False or
                                                  PointStoreModel.fault_message != self.fault_message)) \
            .update({
                PointStoreModel.fault: self.fault,
                PointStoreModel.fault_message: self.fault_message,
            })
