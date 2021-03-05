import sys

from pymodbus.client.sync import ModbusSerialClient


class Modbus():
    def __init__(
            self,
            ip="192.168.0.202",
            port=502,
            timeout=0.1,
            read_info=[]
    ):
        self.ip = ip
        self.port = port
        self.timeout = float(timeout) if str(timeout).isdigit() else 1
        self.read_info = read_info
        # self.modbus_client = ModbusTcpClient(host=self.ip, port=self.port, timeout=self.timeout)
        self.modbus_client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, timeout=0.1, parity='N',
                                                stopbits=1, bytesize=8)
        self.modbus_exception_codes = {
            1: 'Illegal function (type)',
            2: 'Illegal address',
            3: 'Illegal value',
            4: 'Slave failure',
            5: 'Acknowledge',
            6: 'Slave busy',
            8: 'Memory parity error',
            10: 'Gateway path unavailable',
            11: 'Gateway no response'
        }

    def search_slaves(self, search_range='0-0', ping_type=None, ping_addr=None):
        search_range = str(search_range)
        ping_type = int(ping_type)
        ping_addr = int(ping_addr)
        splitted_search_range = search_range.split('-')
        if len(search_range.split('-')) == 2 and all(x.isdigit() for x in splitted_search_range):
            start_slave, end_slave = [int(splitted_search_range[0]), int(splitted_search_range[1])]
            start_slave, end_slave = [start_slave, end_slave] if start_slave < end_slave else [end_slave, start_slave]
            for slave in range(start_slave, end_slave + 1):
                slave_status = 'open'
                try:
                    if ping_type == 1:
                        read_coils = self.modbus_client.read_coils(ping_addr, 1, unit=slave)
                        if read_coils.bits:
                            raw = read_coils.bits
                        else:
                            raw = None
                        print({'slave_status': slave_status, 'address': slave,
                               "raw": raw})
                    if ping_type == 2:
                        read_discrete = self.modbus_client.read_discrete_inputs(ping_addr, 1, unit=slave)
                        if read_discrete.bits:
                            raw = read_discrete.bits
                        else:
                            raw = None
                        print({'slave_status': slave_status, 'address': slave,
                               "raw": raw})
                    if ping_type == 3:
                        read_holding_registers = self.modbus_client.read_holding_registers(ping_addr, 1, unit=slave)
                        if read_holding_registers.registers:
                            registers = read_holding_registers.registers
                            raw = registers[0]
                        else:
                            raw = None
                        print({'slave_status': slave_status, 'address': slave,
                               "raw": raw})
                    if ping_type == 4:
                        read_input_registers = self.modbus_client.read_input_registers(ping_addr, 1, unit=slave)
                        if read_input_registers.registers:
                            registers = read_input_registers.registers
                            raw = registers[0]
                        else:
                            raw = None
                        print({'slave_status': slave_status, 'address': slave,
                               "raw": raw})

                except Exception:
                    slave_status = 'closed'
                    print({'slave_status': slave_status, 'address': slave,
                           "raw": None})
                    pass
        else:
            print({'target': 'slave status', 'data': {'error': 'Invalid input'}})

    def search_addresses(self, search_range='0-0', _slave=None, _coils=None, _discrete=None, _holding=None, _in=None):
        search_range = str(search_range)
        _slave = int(slave)
        _coils = int(_coils)
        _discrete = int(_discrete)
        _holding = int(_holding)
        _in = int(_in)
        print(search_range, _slave, _coils, _discrete, _holding, _input)
        splitted_search_range = search_range.split('-')
        if len(search_range.split('-')) == 2 and all(x.isdigit() for x in splitted_search_range):
            start_address, end_address = [int(splitted_search_range[0]), int(splitted_search_range[1])]
            start_address, end_address = (
                [start_address, end_address]
                if start_address < end_address
                else [end_address, start_address]
            )
            if _coils == 1:
                print("----------------check for read_coils-----------------------------")
                for address in range(start_address, end_address + 1):
                    reg_type = 'coils'
                    try:
                        read_coils = self.modbus_client.read_coils(address, 1, unit=_slave)
                        error = False
                        if read_coils.bits:
                            registers = read_coils.bits
                            raw = registers[0]
                        else:
                            raw = None
                            error = error
                        print({"error": error, 'address': address,
                               'reg_type': reg_type,
                               "raw": raw})
                    except Exception:
                        print({"error": True, 'address': address,
                               'reg_type': reg_type,
                               "raw": None})
            if _discrete == 1:
                print("----------------check for read_discrete_inputs-----------------------------")
                for address in range(start_address, end_address + 1):
                    reg_type = 'd-input'
                    try:
                        read_discrete_input = self.modbus_client.read_discrete_inputs(address, 1, unit=_slave)
                        error = False
                        if read_discrete_input.bits:
                            registers = read_discrete_input.bits
                            raw = registers[0]
                        else:
                            raw = None
                            error = error
                        print({"error": error, 'address': address,
                               'reg_type': reg_type,
                               "raw": raw})

                    except Exception:
                        print({"error": True, 'address': address,
                               'reg_type': reg_type,
                               "raw": None})
            if _holding == 1:
                print("----------------check for read_holding_registers-----------------------------")
                for address in range(start_address, end_address + 1):
                    reg_type = 'holding'
                    try:
                        read_holding_registers = self.modbus_client.read_holding_registers(address, 1, unit=_slave)
                        error = False
                        if read_holding_registers.registers:
                            registers = read_holding_registers.registers
                            raw = registers[0]
                        else:
                            raw = None
                            error = error
                        print({"error": error, 'address': address,
                               'reg_type': reg_type,
                               "raw": raw})

                    except Exception:
                        print({"error": True, 'address': address,
                               'reg_type': reg_type,
                               "raw": None})
            if _in == 1:
                print("----------------check for read_input_registers-----------------------------")
                for address in range(start_address, end_address + 1):
                    reg_type = 'input-r'
                    try:
                        read_input_registers = self.modbus_client.read_input_registers(address, 1, unit=_slave)
                        error = False
                        if read_input_registers.registers:
                            registers = read_input_registers.registers
                            raw = registers[0]
                        else:
                            raw = None
                            error = error
                        print({"error": error, 'address': address,
                               'reg_type': reg_type,
                               "raw": raw})

                    except Exception:
                        print({"error": True, 'address': address,
                               'reg_type': reg_type,
                               "raw": None})

        else:
            print({'target': 'address status', 'data': {'error': 'Invalid input'}})


table = [
    ["type", "code", "number"],
    ["coils", 'FC01', 1],
    ["input-d", 'FC02', 2],
    ["holding", 'FC03', 3],
    ["input-r", 'FC04', 4],
]


def print_table(table):
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))


print("----------------register codes-----------------------------")
print_table(table)
print("----------------***************************----------------")

print("----------------use guide scan for devices-----------------")
print('python test.py scan 0-20 1 1')
print('this will scan slave address from 0 to 20 on coil address 1')
print("----------------***************************-----------------")

print("----------------use guide scan for points on a device-------")
print('python test.py points 0-1 1 1 0 0 1 1')
print('this will scan points on slave 11 for FC03 and FC04 (as they are set to 1 to check and 0 not to check)')
print("----------------***************************------------------")

mod = Modbus()
action = sys.argv[1]

# def search_slaves(self, search_range='0-0', ping_type=None, ping_addr=None):
if action == 'scan':
    print("----------------poll for device's ---------------------------")
    _range = sys.argv[2]
    ping_type = sys.argv[3]
    ping_address = sys.argv[4]
    print(mod.search_slaves(_range, ping_type, ping_address))

# def search_addresses(self, search_range='0-0', slave=None, coils=None, discrete=None, holding=None, _input=None):
if action == 'points':
    print("----------------poll for points ---------------------------")
    _range = sys.argv[2]
    slave = sys.argv[3]
    coils = sys.argv[4]
    discrete = sys.argv[5]
    holding = sys.argv[6]
    _input = sys.argv[7]
    print(mod.search_addresses(_range, slave, coils, discrete, holding, _input))

