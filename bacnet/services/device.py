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

    def get_url(self, device):
        dev_url = f"{device.bac_device_ip}:{device.bac_device_port}"
        bac_device_id = device.bac_device_id
        return {
            "dev_url": dev_url,
            "bac_device_id": bac_device_id
        }

    def get_network(self, device):
        return Network.get_instance().get_network(device.network)

    def get_points(self, device):
        network = self.get_network(device)
        get_url = self.get_url(device)
        dev_url = get_url["dev_url"]
        bac_device_id = get_url["bac_device_id"]
        read = f"{dev_url} device {bac_device_id} objectList"
        return network.read(read)

      # example point/76e9b1e6-4f3e-4391-9aba-93e1881ecfe4/analogInput/1/presentValue  
    def get_point(self, device, obj, obj_instance, prop):
        get_url = self.get_url(device)
        network = self.get_network(device)
        dev_url = get_url["dev_url"]
        read = f"{dev_url} {obj} {obj_instance} {prop}"
        print(read)

        return network.read(read)
