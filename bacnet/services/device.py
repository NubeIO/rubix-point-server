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


    # def get_points(self, device):
    #     print("device", device)
    #     dev_url = f"{device.bac_device_ip}:{device.bac_device_port}"
    #     bac_device_id = device.bac_device_id

    #     network = Network.get_instance().get_network(device.network)
    #     return network.read(f"{dev_url} device {bac_device_id} objectList")

    def get_points(self, device):
        network = self.get_network(device)
        get_url = self.get_url(device)
    
        dev_url = get_url["dev_url"]
        bac_device_id = get_url["bac_device_id"]
        read = f"{dev_url} device {bac_device_id} objectList"
        print(222222)
        print("device", device)
        print("get_url", get_url)
        print('network', network)
        print("read", read)
        return network.read(read)
        
    def get_point(self, device, obj, obj_instance, prop):

        # address = test_device_url
        # obj = pnt_type
        # obj_instance = pnt_id
        # prop = "presentValue"

        # readObj  = f"{test_device_url} {obj} {obj_instance} {prop}"
        # read = bacnet.read(readObj)
        get_url = self.get_url(device)
        network = self.get_network(device)
        dev_url = get_url["dev_url"]
        # bac_device_id = get_url["bac_device_id"]
        read = f"{dev_url} {obj} {obj_instance} {prop}"
        print(read)

        return network.read(read)
