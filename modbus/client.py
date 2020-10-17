import json
from modbus.modbus_master import TCP_Client, RTU_Client, Master


class Client:
    def __init__(self, path, client_type):
        self.path = path
        self.client_type = client_type

    def _open_config(self):
        with open(self.path) as json_file:
            return json.load(json_file)

    def get_parm(self):
        _config = self._open_config()
        _dict_parm = _config['client'][self.client_type]
        return _dict_parm

    def make_client(self):
        _master = None
        _parm = self.get_parm().values()
        if self.client_type == 'tcp':
            _master = TCP_Client(*_parm)
        if self.client_type == 'rtu':
            _master = RTU_Client(*_parm)
        _client = _master.client
        return Master(_client)  # calling the Master class in the API


# ===================================================================================================================

class Reading:
    def __init__(self, client, unit, reg_start, reg_length, **kwargs):
        self.client = client
        self.unit = unit
        self.reg_start = reg_start
        self.reg_length = reg_length

    def reg_address(self):
        return self.reg_start

    def set_reg_address(self, address):
        self.reg_start = address

    def length_data(self):
        return self.reg_length

    def set_length_data(self, size):
        self.reg_length = size


# ====================================================================================================================

class Registers(Reading):

    def __init__(self, client, unit, reg_start, reg_length, data_type, transp=True):
        super().__init__(client, unit, reg_start, reg_length)
        self.data_type = data_type
        self.transp = transp

    def _read_reg(self):
        return self.client.read_register(self.unit, self.reg_start,
                                         self.reg_length, self.reg_type,
                                         self.data_type, self.transp)

    def read_holding(self):
        self.reg_type = 'holding'
        return self._read_reg()

    def read_input(self):
        self.reg_type = 'input'
        return self._read_reg()


# ===================================================================================================================

class Coils(Reading):

    def __init__(self, client, unit, reg_start, reg_length):
        super().__init__(client, unit, reg_start, reg_length)

    def _read_coil(self):
        return self.client.read_coil(self.unit, self.reg_start, self.reg_length)

    def read_coil(self):
        self.reg_type = 'coil'
        return self.read_coil()
