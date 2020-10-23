from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

client = ModbusClient(method="rtu", port="/dev/ttyUSB0", stopbits=1, bytesize=8, parity='N', baudrate=9600)
connection = client.connect()
result = client.read_holding_registers(1, 2, unit=1)
print(result)

client.close()
