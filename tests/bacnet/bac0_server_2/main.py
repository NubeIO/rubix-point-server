import BAC0
from BAC0.core.utils.notes import note_and_log
import time
from tests.bacnet.bac0_server_2.bacnet_device import device


@note_and_log
class App(object):
    def __init__(self, ip, device_id):
        self.dev = device(ip=ip, device_id=device_id)


def main():
    BAC0.log_level("debug")
    app = App(ip='192.168.0.101/24:47808', device_id=123)
    app._log.debug("Starting processing values task")
    while True:
        time.sleep(20)


if __name__ == "__main__":
    main()
