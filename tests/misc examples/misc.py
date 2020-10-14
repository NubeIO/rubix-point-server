from os import remove
from os.path import exists
from commons import addlog, init_log
from time import sleep

_debug = True

@addlog
class Vdev:
    """
    Using a file to simulate a dev.
    """
    def __init__(self, file):
        if _debug: Vdev.debug("Vdev: create file: %s" % file)
        self.file = file

    def write(self, value=None):
        raise NotImplementedError("Write access not allowed.")

    def read(self):
        raise NotImplementedError("Readd access not allowed.")


class VBIdev(Vdev):
    """
    Binary Input device. 0 / 1
    """
    def __init__(self, num, default='0'):
        print("VBIdev Input", num, default)
        # Vdev.__init__(self, "./dev/BI.dev-"+str(num))
        # with open(self.file, 'w', encoding='UTF-8') as f:
        #     f.write(default)

    def read(self):
        return "inactive"
        # with open(self.file, 'r', encoding='UTF-8') as f:
        #     c = f.read(1)
        #     return "inactive" if c == '0' else "active"


class VBOdev(Vdev):
    """
    Binary Output device. 0 / 1
    """
    def __init__(self, num, default='0'):
        print("VBOdev write", num, default)
        # Vdev.__init__(self, "./dev/BO.dev-"+str(num))
        # with open(self.file, 'w', encoding='UTF-8') as f:
        #     f.write(default)

    def write(self, value):
        print("VBOdev write", value)
        # with open(self.file, 'w', encoding='UTF-8') as f:
        #     f.write('0') if value == "inactive" else f.write('1')

    def read(self):
        return "inactive"
        # with open(self.file, 'r', encoding='UTF-8') as f:
        #     c = f.read(1)
        #     return "inactive" if c == '0' else "active"

if __name__ == '__main__':
    init_log(level="DEBUG")
    vi = VBIdev(1)
    vo = VBOdev(0)
    sleep(10)

