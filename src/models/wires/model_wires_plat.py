from src import db


class WiresPlatModel(db.Model):
    __tablename__ = 'wires_plat'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    device_name = db.Column(db.String(80), nullable=False)
    client_id = db.Column(db.String(80), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    site_id = db.Column(db.String(80), nullable=False)
    site_name = db.Column(db.String(80), nullable=False)
    site_address = db.Column(db.String(80), nullable=False)
    site_city = db.Column(db.String(80), nullable=False)
    site_state = db.Column(db.String(80), nullable=False)
    site_zip = db.Column(db.String(80), nullable=False)
    site_country = db.Column(db.String(80), nullable=False)
    site_lat = db.Column(db.String(80), nullable=False)
    site_lon = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"Wires(uuid = {self.uuid})"

    @classmethod
    def find_by_uuid(cls, wires_uuid):
        return cls.query.filter_by(uuid=wires_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
