from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.compat import iteritems
from collections import OrderedDict
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=3,
    parity='N',
    stopbits=1,
    bytesize=8
)


address = 0
count = 30
unit = 1


result = client.read_holding_registers(address, count, unit=unit)
print(result.registers)

bo = Endian.Big
wo = Endian.Big
result = client.read_holding_registers(address, count, unit=unit)
decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                             byteorder=bo,
                                             wordorder=wo)

print("Big, Big", decoder.decode_32bit_float())


bo = Endian.Big
wo = Endian.Little
decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                             byteorder=bo,
                                             wordorder=wo)

print("Big, Little", decoder.decode_32bit_float())

bo = Endian.Little
wo = Endian.Big
decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                             byteorder=bo,
                                             wordorder=wo)

print("Little, Big", decoder.decode_32bit_float())

bo = Endian.Little
wo = Endian.Little
decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                             byteorder=bo,
                                             wordorder=wo)

print("Little, Little", decoder.decode_32bit_float())