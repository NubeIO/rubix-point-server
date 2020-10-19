from src import db


class ModbusPointStoreModel(db.Model):
    __tablename__ = 'mod_points_store'
    mod_point_store_uuid = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    mod_point_value = db.Column(db.Float(), nullable=True)
    mod_point_uuid = db.Column(db.String, db.ForeignKey('mod_points.mod_point_uuid'))

    def __repr__(self):
        return f"ModbusPointStore(mod_point_store_uuid = {self.mod_point_uuid})"

    @classmethod
    def find_by_uuid(cls, mod_point_uuid):
        return cls.query.filter_by(mod_point_uuid=mod_point_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
