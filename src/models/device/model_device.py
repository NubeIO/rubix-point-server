from src import db


class DeviceModel(db.Model):
    __tablename__ = 'devices'
    device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_name = db.Column(db.String(80), nullable=False)
    device_enable = db.Column(db.String(80), nullable=False)
    device_fault = db.Column(db.Boolean(), nullable=True)
    device_network_uuid = db.Column(db.String, db.ForeignKey('networks.network_uuid'), nullable=False)
    device_points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)
    device_driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'device',
        'polymorphic_on': device_driver
    }

    def __repr__(self):
        return f"Device(device_uuid = {self.device_uuid})"

    @classmethod
    def find_by_device_uuid(cls, device_uuid):
        return cls.query.filter_by(device_uuid=device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
