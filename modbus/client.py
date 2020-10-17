import json
import time

from Modbus_API.modbus_master import TCP_Client, RTU_Client, Master


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
    def __init__(self, client, unit, reg_start, reg_lenght, **kwargs):
        self.client = client
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght

    def reg_adress(self):
        return self.reg_start

    def set_reg_adress(self, adress):
        self.reg_start = adress

    def lenght_data(self):
        return self.reg_lenght

    def set_lenght_data(self, size):
        self.reg_lenght = size


# ====================================================================================================================

class Registers(Reading):

    def __init__(self, client, unit, reg_start, reg_lenght, data_type, transp=True):
        super().__init__(client, unit, reg_start, reg_lenght)
        self.data_type = data_type
        self.transp = transp

    def _read_reg(self):
        return self.client.read_register(self.unit, self.reg_start,
                                         self.reg_lenght, self.reg_type,
                                         self.data_type, self.transp)

    def read_holding(self):
        self.reg_type = 'holding'
        return self._read_reg()

    def read_input(self):
        self.reg_type = 'input'
        return self._read_reg()


# ===================================================================================================================

class Coils(Reading):

    def __init__(self, client, unit, reg_start, reg_lenght):
        super().__init__(client, unit, reg_start, reg_lenght)

    def _read_boll(self):
        return self.client.read_bool(self.unit, self.reg_start, self.reg_lenght)

    def read_coil(self):
        self.reg_type = 'coil'
        return self._read_boll()


# ====================================================================================================================

# if __name__ == '__main__':
#
#     modbus = Client('config.json', 'tcp')
#     client = modbus.make_client()
#     print(modbus.get_parm())
#
#     # reg_for_check = [30201, 30233, 30531, 30775, 30795, 30803, 30805, 30813, 30837, 30839, 30769, 30771, 30773,
#     #                  30957, 30959, 30961, 30537, 30953, 40212, 40915]
#
#     reg = Registers(client, unit=1, reg_start=1000, reg_lenght=16, data_type='int')
#     bol = Coils(client, unit=1, reg_start=0, reg_lenght=250)
#
#     reg_for_check = [i for i in range(1000, 1016)]
#     nr = 1
#
#
#     def print_data(time, data):
#         return print("{} : {}".format(time, data), end=';\n')
#
#
#     try:
#         while True:
#             # reg.set_reg_adress(0)
#             # reg.set_lenght_data(nr)
#             # bol.set_lenght_data(nr)
#             holding = reg.read_holding()
#             time.sleep(1)
#             col = bol.read_coil()
#             print_data(holding['Time'][1], holding['Data'])
#             print_data(col['Time'][1], col['Data'])
#             nr += 1
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print('\nEnd')
