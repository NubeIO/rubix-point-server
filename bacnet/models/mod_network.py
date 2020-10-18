from bacnet import db


class ModNetworkModel(db.Model):
    __tablename__ = 'mod_networks'
    mod_network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_network_name = db.Column(db.String(80), nullable=False)
    mod_network_ip = db.Column(db.String(80), nullable=False)
    mod_network_port = db.Column(db.Integer(), nullable=False)
    # network_device_id = db.Column(db.Integer(), nullable=False)
    # network_device_name = db.Column(db.String(80), nullable=False)
    # network_number = db.Column(db.Integer())
    # mod_devices = db.relationship('ModDeviceModel', cascade="all,delete", backref='mod_network', lazy=True)

    def __repr__(self):
        return f"Network(mod_network_uuid = {self.mod_network_uuid})"

    @classmethod
    def find_by_network_uuid(cls, mod_network_uuid):
        return cls.query.filter_by(mod_network_uuid=mod_network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
