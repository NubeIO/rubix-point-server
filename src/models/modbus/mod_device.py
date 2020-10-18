from src import db


class ModbusDeviceModel(db.Model):
    __tablename__ = 'mod_devices'
    mod_device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    mod_device_name = db.Column(db.String(80), nullable=False)
    mod_device_enable = db.Column(db.String(80), nullable=False)
    mod_device_type = db.Column(db.String(80), nullable=False)
    mod_device_addr = db.Column(db.Integer(), nullable=False)
    mod_tcp_device_ip = db.Column(db.String(80), nullable=False)
    mod_tcp_device_port = db.Column(db.Integer(), nullable=False)
    mod_ping_point_type = db.Column(db.String(80), nullable=False)
    mod_ping_point_address = db.Column(db.Integer(), nullable=False)
    mod_network_zero_mode = db.Column(db.Boolean(), nullable=False)
    mod_device_timeout = db.Column(db.Integer(), nullable=False)
    mod_device_timeout_global = db.Column(db.Boolean(), nullable=False)

    # network_number = db.Column(db.Integer())

    # mod_network_uuid = db.Column(db.String, db.ForeignKey('mod_networks.mod_network_uuid'))
    # mod_devices = db.relationship('ModDeviceModel', cascade="all,delete", backref='mod_network', lazy=True)

    def __repr__(self):
        return f"Device(mod_device_uuid = {self.mod_device_uuid})"

    @classmethod
    def find_by_device_uuid(cls, mod_device_uuid):
        return cls.query.filter_by(mod_device_uuid=mod_device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
