from models.network import NetworkModel
from db import db
import requests
import BAC0


def init_bac_network(ip, instance, name):
    net = BAC0.lite(ip=ip, deviceId=instance, localObjName=name)
    return net


def init_bac_device(ip, instance, net):
    controller = BAC0.device(ip, instance, net,poll=0, history_size=0)
    return controller


def terminate_net(net):
    net.disconnect()
    print('Its over')


# def terminate_dev(self, dev):
#     dev.disconnect(save_on_disconnect=False, unregister=True)
#     print('Its over')


# def terminate():
#     global bacnet
#     bacnet.disconnect()
#     print('Its over')


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
                'bac_device_port': self.bac_device_port, 'network_uuid': self.network_uuid}

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
    def join_net_device_rest(cls, dev_uuid, net_uuid):
        from app import ip, port, api_ver
        url = f'http://{ip}:{port}/{api_ver}'

        network_uuid = net_uuid
        device_uuid = dev_uuid
        networks = requests.get(f'{url}/network/{network_uuid}')
        networks_as_json = networks.json()
        print(networks_as_json)
        print("TYPE OFF:", type(networks_as_json))
        # print(networks_as_json)
        response = networks_as_json
        network_uuid = response['network_uuid']
        network_ip = response['network_ip']
        network_mask = response['network_mask']
        network_port = response['network_port']
        network_device_id = response['network_device_id']
        network_device_name = response['network_device_name']
        print(f'{url}/device/{device_uuid}')
        devices = requests.get(f'{url}/device/{device_uuid}')
        response_device = devices.json()

        print(response_device)

        bac_device_uuid = response_device['bac_device_uuid']
        bac_device_mac = response_device['bac_device_mac']
        bac_device_id = response_device['bac_device_id']
        bac_device_ip = response_device['bac_device_ip']
        bac_device_port = response_device['bac_device_port']
        bac_network_uuid = response_device['network_uuid']
        bac_network_uuid = response_device['network_uuid']
        # ip = '192.168.0.100/24:47808'
        net_url = f'{network_ip}/{network_mask}:{network_port}'
        print(net_url)
        bacnet_network = {
            'net_url': net_url,
            'network_device_id': network_device_id,
            'network_device_name': network_device_name
        }

        net = init_bac_network(bacnet_network['net_url'], bacnet_network['network_device_id'],
                               bacnet_network['network_device_name'])

        dev_url = f'{bac_device_ip}:{bac_device_port}'

        bacnet_device = {
            'dev_url': dev_url,
            'bac_device_id': bac_device_id,

        }

        print(bacnet_network)
        print(bacnet_device)
        # dev = BAC0.device(bacnet_device['dev_url'], bacnet_device['bac_device_id'], net, poll=0, history_size=0)

        dev = init_bac_device(bacnet_device['dev_url'], bacnet_device['bac_device_id'], net)
        print(dev.points)
        response = {
            'network_uuid': network_uuid,
            'bac_network_uuid': bac_network_uuid,
            'bac_device_id': bac_device_id,
            'bac_device_mac': bac_device_mac,
            # 'points': dev.points)
        }
        print(11111)
        print(response)
        terminate_net(net)
        # terminate_dev(dev)
        # print(bacnet_device['dev_url'])
        return 222

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
