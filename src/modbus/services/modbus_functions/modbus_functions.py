import time
import sys
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger("SDM630_READER")
log.setLevel(logging.INFO)


def read_holding(client, reg_start, reg_length, _unit):
    """
    Auxiliary function
    :return:holding reg
    """
    reg_type = 'holding'
    read = client.read_holding_registers(reg_start, reg_length, unit=_unit)
    if _assertion(read, client, reg_type) == False:  # checking for errors
        return read.registers


def _assertion(operation, client, reg_type):
    """
    :param operation: Client method. Checks whether data has been downloaded
    :return: Status False to OK or True.
    """
    # test that we are not an error
    if not operation.isError():
        pass
    else:
        print("connects to port: {}; Type Register: {}; Exception: {}".format(client.port,
                                                                              reg_type,
                                                                              operation, ))
    return operation.isError()


from pymodbus.client.sync import ModbusTcpClient as ModbusClient, ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

# HOST = '127.0.0.1'
# PORT = 555
# UNIT = 1
# INTERVAL = 5

SLAVES = {
    "SLAVE_1": {
        "host": "0.0.0.0",
        "port": 8502,
        "unit": 1,
    },
    "SLAVE_2": {
        "host": "0.0.0.0",
        "port": 8503,
        "unit": 1,
    }
}

POINTS = {
    "PNT_1": {
        "name": "name 111",
        "reg_start": 11,
        "reg_lenght": 2,

    },
    "PNT_2": {
        "name": "name 222",
        "reg_start": 22,
        "reg_lenght": 2,
    },
    "PNT_3": {
        "name": "name 333",
        "reg_start": 33,
        "reg_lenght": 2,
    }

}
cnt = 1

try:
    while True:
        time.sleep(2)
        for key, slave in SLAVES.items():
            # log.info("Handling slave=%s", slave)
            cnt += 1
            for key, point in POINTS.items():
                try:
                    reg = point["reg_start"]
                    host = slave["host"]
                    port = slave["port"]
                    unit = slave["unit"]
                    # print(cnt)

                    modbus = ModbusTcpClient(host, port)
                    # val = modbus.read_holding_registers(reg, 1, unit=unit)
                    val = read_holding(modbus, reg, 1, _unit=unit)
                    print(val)

                    # val.bits[0:] for coils/inputs
                    # val.register[0:] for holding
                    # print('val', val.registers[0:], 'poll_count', cnt, 'slave', slave, 'reg', reg)
                    # print(read)
                except:
                    log.error(
                        "Error handling register %s for slave=%s!", key, slave)
                    # traceback.print_exc()

except KeyboardInterrupt:
    print('\nEnd')