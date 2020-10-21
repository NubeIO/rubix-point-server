from pymodbus.client.sync import ModbusSerialClient
import logging

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

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
    '''Reading from a holding register with the below content.'''
    res = client.read_holding_registers(6, 10, unit=1)
    print(res.registers, "res")
    decoder = BinaryPayloadDecoder.fromRegisters(res.registers,
                                                 byteorder=bo,
                                                 wordorder=wo).decode_32bit_float()
    print(decoder, "decoder")



    '''Reading from a discrete register with the below content.'''
    # res = client.read_discrete_inputs(address=1, count=1, unit=1)

    if not res.isError():
        # print(res.registers)
        print(res)
    else:
        # print(res)
        print(res)

else:
    print('Cannot connect to the Modbus Server/Slave')