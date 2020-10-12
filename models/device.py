from models.network import NetworkModel
from db import db
import requests

class DeviceModel(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    bac_device_uuid = db.Column(db.String(80), unique=True, nullable=False)
    bac_device_mac = db.Column(db.Integer(), unique=False, nullable=False)
    bac_device_id = db.Column(db.Integer(), unique=False, nullable=False)
    bac_device_ip = db.Column(db.String(20), unique=False, nullable=False)
    bac_device_mask = db.Column(db.Integer(), nullable=False)
    bac_device_port = db.Column(db.Integer(), nullable=False)
    network_uuid = db.Column(db.Integer, db.ForeignKey('networks.network_uuid'))
    network = db.relationship('NetworkModel')

    def __init__(self, bac_device_uuid, bac_device_mac, bac_device_id, bac_device_ip, bac_device_mask, bac_device_port,
                 network_uuid):
        self.bac_device_uuid = bac_device_uuid
        self.bac_device_mac = bac_device_mac
        self.bac_device_id = bac_device_id
        self.bac_device_ip = bac_device_ip
        self.bac_device_mask = bac_device_mask
        self.bac_device_port = bac_device_port
        self.network_uuid = network_uuid

    def get_device(self):
        return {'bac_device_uuid': self.bac_device_uuid, 'bac_device_mac': self.bac_device_mac,
                'bac_device_id': self.bac_device_id, 'bac_device_ip': self.bac_device_ip,
                'network_uuid': self.network_uuid}

    def item_uuid(self):
        return {'bac_device_uuid': self.bac_device_uuid}

    @classmethod
    def find_by_bac_device_uuid(cls, bac_device_uuid):
        return cls.query.filter_by(bac_device_uuid=bac_device_uuid).first()

    @classmethod
    def join_net_device(cls, uuid):
        print(uuid)
        get_devices = cls.query.session.query(DeviceModel, NetworkModel).join(NetworkModel).filter(
            NetworkModel.network_uuid == uuid).all()
        return get_devices

    @classmethod
    def join_net_device_rest(cls, uuid):
        # api.add_resource(Device, f'/{api_ver}/device/<string:name>')
        devices = requests.get('http://127.0.0.1:5000/api/1.1/devices')
        networks = requests.get('http://127.0.0.1:5000/api/1.1/networks')


        return networks

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
