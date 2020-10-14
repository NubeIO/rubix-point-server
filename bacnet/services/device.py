from bacnet.services.network import Network


class Device:
    __instance = None

    @staticmethod
    def get_instance():
        if Device.__instance is None:
            Device()
        return Device.__instance

    def __init__(self):
        if Device.__instance is not None:
            raise Exception("Device class is a singleton!")
        else:
            Device.__instance = self

    def get_points(self, device):
        dev_url = f"{device.bac_device_ip}:{device.bac_device_port}"
        bac_device_id = device.bac_device_id

        network = Network.get_instance().get_network(device.network)
        if network:
            return network.read(f"{dev_url} device {bac_device_id} objectList")
        return []
