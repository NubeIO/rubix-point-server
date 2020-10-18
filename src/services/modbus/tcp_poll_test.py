# This is a simulator script that connects to a modbus slave device and
# writes the CPU temperature for the raspberry pi device to a modbus register.
# If an exception occurs, it will wait 5 seconds and try again.

import time
import sys
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger("SDM630_READER")
log.setLevel(logging.INFO)

from pymodbus.client.sync import ModbusTcpClient as ModbusClient, ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

HOST = '127.0.0.1'
PORT = 5020
UNIT = 1
INTERVAL = 5

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
        "reg_start": 10001,
        "reg_lenght": 2,

    },
    "PNT_2": {
        "name": "name 222",
        "reg_start": 10002,
        "reg_lenght": 2,
    },
    "PNT_3": {
        "name": "name 333",
        "reg_start": 10003,
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
                    val = modbus.read_holding_registers(reg, 1, unit=unit)

                    # val.bits[0:] for coils/inputs
                    # val.register[0:] for holding
                    print('val', val.registers[0:], 'poll_count', cnt, 'slave', slave, 'reg', reg)
                    # print(read)
                except:
                    log.error(
                        "Error handling register %s for slave=%s!", key, slave)
                    # traceback.print_exc()

except KeyboardInterrupt:
    print('\nEnd')
