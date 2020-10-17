from bacnet import db


class ModDeviceModel(db.Model):
    __tablename__ = 'mod_devices'
    bac_device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=False, nullable=False)
    unit = db.Column(db.Integer(), unique=False, nullable=False)
    mod_network_uuid = db.Column(db.String, db.ForeignKey('mod_networks.network_uuid'))

    def __repr__(self):
        return f"Device(mod_device_uuid = {self.network_uuid})"

    @classmethod
    def find_by_mod_device_uuid(cls, mod_device_uuid):
        return cls.query.filter_by(mod_device_uuid=mod_device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
