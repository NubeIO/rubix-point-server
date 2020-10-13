import BAC0


class Services:
    __instance = None

    @staticmethod
    def get_instance():
        if not Services.__instance:
            Services()
        return Services.__instance

    def __init__(self):
        if not Services.__instance:
            raise Exception("This class is a singleton!")
        else:
            Services.__instance = self
            self.networks = {}

    def add_network(self, network):
        net_url = f'{network.network_ip}/{network.network_mask}:{network.network_port}'
        network_device_id = network.network_device_id
        network_device_name = network.network_device_name

        if not self.networks[net_url]:
            self.networks[net_url] = {}

        if not self.networks[net_url][network_device_id]:
            self.networks[net_url][network_device_id] = {}

        self.networks[net_url][network_device_id][network_device_name] = \
            BAC0.lite(ip=net_url, deviceId=network_device_id, localObjName=network_device_name)

    def remove_network(self, network):
        net_url = f'{network.network_ip}/{network.network_mask}:{network.network_port}'
        network_device_id = network.network_device_id
        network_device_name = network.network_device_name

        if self.networks.get(net_url, {}).get(network_device_id, {}).get(network_device_name):
            del self.networks[net_url][network_device_id][network_device_name]
