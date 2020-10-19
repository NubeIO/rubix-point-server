import BAC0
from src.bacnet.models.network import NetworkModel


class Network:
    __instance = None

    @staticmethod
    def get_instance():
        if not Network.__instance:
            Network()
        return Network.__instance

    def __init__(self):
        if Network.__instance:
            raise Exception("Network class is a singleton!")
        else:
            Network.__instance = self
            self.networks = {}

    def start(self):
        print("Network Start...")
        network_service = Network.get_instance()
        for network in NetworkModel.query.all():
            network_service.add_network(network)

    def add_network(self, network):
        net_url = f"{network.network_ip}/{network.network_mask}:{network.network_port}"
        network_device_id = network.network_device_id
        network_device_name = network.network_device_name

        if not self.networks.get(net_url):
            self.networks[net_url] = {}

        if not self.networks.get(net_url).get(network_device_id):
            self.networks[net_url][network_device_id] = {}

        print('=====================================================')
        print('...........Creating BACnet network with..............')
        print('net_url:', net_url)
        print('network_device_id:', network_device_id)
        print('network_device_name:', network_device_name)
        print('.....................................................')
        print('=====================================================')

        try:
            network = BAC0.lite(ip=net_url, deviceId=network_device_id, localObjName=network_device_name)
            self.networks[net_url][network_device_id][network_device_name] = network

        except:
            print("Initialization error!")

    def delete_network(self, network):
        net_url = f"{network.network_ip}/{network.network_mask}:{network.network_port}"
        network_device_id = network.network_device_id
        network_device_name = network.network_device_name

        network = self.networks.get(net_url, {}).get(network_device_id, {}).get(network_device_name)
        if network:
            pass
            # TODO: uncomment, disconnect is not working fine
            # network.disconnect()
            # del self.networks[net_url][network_device_id][network_device_name]

    def get_network(self, network):
        net_url = f'{network.network_ip}/{network.network_mask}:{network.network_port}'
        network_device_id = network.network_device_id
        network_device_name = network.network_device_name
        return self.networks.get(net_url, {}).get(network_device_id, {}).get(network_device_name)
