from src import db


class DeviceModel(db.Model):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_uuid = db.Column(db.String, db.ForeignKey('networks.uuid'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.String(80), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    history_enable = db.Column(db.Boolean(), nullable=False, default=True)
    points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)
    driver = db.Column(db.String(80))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'device',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Device(device_uuid = {self.device_uuid})"

    @classmethod
    def find_by_uuid(cls, device_uuid):
        return cls.query.filter_by(uuid=device_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
