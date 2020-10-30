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
        return f"Wires({self.uuid})"

    @classmethod
    def find_by_uuid(cls, wires_uuid):
        return cls.query.filter_by(uuid=wires_uuid).first()

    @classmethod
    def filter_by_uuid(cls, wires_uuid):
        return cls.query.filter_by(uuid=wires_uuid)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls):
        db.session.query(WiresPlatModel).delete()
        db.session.commit()

    @classmethod
    def update_to_db(cls, _uuid, data):
        cls.filter_by_uuid(_uuid).update({**data, "uuid": _uuid})
        db.session.commit()
