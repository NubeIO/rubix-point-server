from bacnet.models.mod_network import ModNetworkModel

class ModNetwork:
    __instance = None

    @staticmethod
    def get_instance():
        if not ModNetwork.__instance:
            ModNetwork()
        return ModNetwork.__instance

    def __init__(self):
        if ModNetwork.__instance:
            raise Exception("Network class is a singleton!")
        else:
            ModNetwork.__instance = self
            self.networks = {}

    def start(self):
        print("Network Start...")
        network_service = ModNetwork.get_instance()
        for network in ModNetworkModel.query.all():
            network_service.add_network(network)

    def add_network(self, network):
        net_url = f"{network.mod_network_ip}:{network.mod_network_port}"
        # mod_network_device_id = network.mod_network_device_id
        mod_network_name = network.mod_network_name

        if not self.networks.get(net_url):
            self.networks[net_url] = {}


        print('=====================================================')
        print('...........Creating Modbus network with..............')
        print('net_url:', net_url)
        print('network_device_name:', mod_network_name)
        print('.....................................................')
        print('=====================================================')

        # try:
        #     network = BAC0.lite(ip=net_url, deviceId=network_device_id, localObjName=network_device_name)
        #     self.networks[net_url][network_device_id][network_device_name] = network
        #
        # except:
        #     print("Initialization error!")

    def delete_network(self, network):
        net_url = f"{network.mod_network_ip}:{network.mod_network_port}"
        # mod_network_device_id = network.mod_network_device_id
        mod_network_name = network.mod_network_name

        network = self.networks.get(net_url, {}).get(mod_network_name)
        if network:
            pass
            # TODO: uncomment, disconnect is not working fine
            # network.disconnect()
            # del self.networks[net_url][network_device_id][network_device_name]

    def get_network(self, network):
        net_url = f"{network.mod_network_ip}/{network.mod_network_port}"
        # mod_network_device_id = network.mod_network_device_id
        mod_network_name = network.mod_network_name
        return self.networks.get(net_url, {}).get(mod_network_name)
