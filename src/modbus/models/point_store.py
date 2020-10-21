from src import db


class ModbusPointStoreModel(db.Model):
    __tablename__ = 'mod_points_store'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    value = db.Column(db.Float(), nullable=False)
    point_uuid = db.Column(db.String, db.ForeignKey('mod_points.uuid'), nullable=False)

    def __repr__(self):
        return f"ModbusPointStore({self.id})"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
