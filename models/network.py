from db import db


class NetworkModel(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    ip = db.Column(db.String(20), unique=False, nullable=False)
    mask = db.Column(db.Integer(), nullable=False)
    port = db.Column(db.Integer(), nullable=False)
    network_number = db.Column(db.Integer())
    # devices = db.relationship('DeviceModel', lazy='dynamic')

    def __init__(self, uuid, ip, mask, port, network_number):
        self.uuid = uuid
        self.ip = ip
        self.mask = mask
        self.port = port
        self.network_number = network_number
        # self.devices = devices

    def get_network(self):
        return {
            'network_uuid': self.uuid,
            'ip': self.ip,
            'mask': self.mask,
            'port': self.port,
            'bacnet_network_id': self.network_number,
            # 'device':  [device.json() for device in self.devices.all()]
        }

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
