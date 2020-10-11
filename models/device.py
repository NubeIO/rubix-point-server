from db import db


class DeviceModel(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), unique=True, nullable=False)
    mac = db.Column(db.Integer(), unique=False, nullable=False)
    bac_device_id = db.Column(db.Integer(), unique=False, nullable=False)
    ip = db.Column(db.String(20), unique=False, nullable=False)
    mask = db.Column(db.Integer(), nullable=False)
    port = db.Column(db.Integer(), nullable=False)
    network_uuid = db.Column(db.Integer, db.ForeignKey('networks.uuid')) 
    network = db.relationship('NetworkModel')

    def __init__(self, uuid, mac, bac_device_id, ip, mask, port, network_uuid):
        self.uuid = uuid
        self.mac = mac
        self.bac_device_id = bac_device_id
        self.ip = ip
        self.mask = mask
        self.port = port
        self.network_uuid = network_uuid

    def get_device(self):
        return {'uuid': self.uuid, 'mac': self.mac, 'bac_device_id': self.bac_device_id, 'ip': self.ip, 'network_uuid': self.network_uuid}

    def item_uuid(self):
        return {'uuid': self.uuid}

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
