import logging

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=3,
    parity='N',
    stopbits=1,
    bytesize=8
)
bo = Endian.Big
wo = Endian.Big

if client.connect():  # Trying for connect to Modbus Server/Slave
    builder = BinaryPayloadBuilder(byteorder=bo, wordorder=wo)
    builder.add_32bit_float(33.333333)
    payload = builder.to_registers()
    print(payload)
    result = client.write_registers(9086, payload, unit=1)

    if not result.isError():
        print(result)
    else:
        print(result)
