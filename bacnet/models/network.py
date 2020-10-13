from bacnet import db


class NetworkModel(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    network_uuid = db.Column(db.String(80), unique=True, nullable=False)
    network_ip = db.Column(db.String(20), unique=False, nullable=False)
    network_mask = db.Column(db.Integer(), nullable=False)
    network_port = db.Column(db.Integer(), nullable=False)
    network_device_id = db.Column(db.Integer(), nullable=False)
    network_device_name = db.Column(db.String(80), nullable=False)
    network_number = db.Column(db.Integer())

    # devices = db.relationship('DeviceModel', lazy='dynamic')

    def __init__(self, network_uuid, network_ip, network_mask, network_port, network_number, network_device_id,
                 network_device_name):
        self.network_uuid = network_uuid
        self.network_ip = network_ip
        self.network_mask = network_mask
        self.network_port = network_port
        self.network_number = network_number
        self.network_device_id = network_device_id
        self.network_device_name = network_device_name

        # self.devices = devices

    def get_network(self):
        return {
            'network_uuid': self.network_uuid,
            'network_ip': self.network_ip,
            'network_mask': self.network_mask,
            'network_port': self.network_port,
            'bacnet_network_id': self.network_number,
            'network_device_id': self.network_device_id,
            'network_device_name': self.network_device_name,
            # 'device':  [device.json() for device in self.devices.all()]
        }

    def get_network_ids(self):
        return {
            'network_uuid': self.network_uuid,
        }

    @classmethod
    def find_by_network_uuid(cls, network_uuid):
        return cls.query.filter_by(network_uuid=network_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
