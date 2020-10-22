from src import db


class NetworkModel(db.Model):
    __tablename__ = 'networks'
    network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_name = db.Column(db.String(80), nullable=False)
    network_enable = db.Column(db.Boolean(), nullable=False)
    network_fault = db.Column(db.Boolean(), nullable=True)
    network_devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)
    network_driver = db.Column(db.String(80))

    __mapper_args__ = {
        'polymorphic_identity': 'network',
        'polymorphic_on': network_driver
    }

    def __repr__(self):
        return f"Network(network_uuid = {self.network_uuid})"

    @classmethod
    def find_by_network_uuid(cls, network_uuid):
        return cls.query.filter_by(network_uuid=network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
