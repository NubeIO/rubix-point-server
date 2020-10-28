from src import db


class NetworkModel(db.Model):
    __tablename__ = 'networks'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Boolean(), nullable=True)
    devices = db.relationship('DeviceModel', cascade="all,delete", backref='network', lazy=True)
    driver = db.Column(db.String(80))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'network',
        'polymorphic_on': driver
    }

    def __repr__(self):
        return f"Network(uuid = {self.uuid})"

    @classmethod
    def find_by_uuid(cls, network_uuid):
        return cls.query.filter_by(uuid=network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
