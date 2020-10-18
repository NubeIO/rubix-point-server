from src import db


class ModbusPointModel(db.Model):
    __tablename__ = 'mod_points'
    mod_point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_point_name = db.Column(db.String(80), nullable=False)
    mod_point_reg = db.Column(db.String(80), nullable=False)
    # devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)

    def __repr__(self):
        return f"Point(mod_point_uuid = {self.mod_point_uuid})"

    @classmethod
    def find_by_uuid(cls, mod_point_uuid):
        return cls.query.filter_by(mod_point_uuid=mod_point_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
