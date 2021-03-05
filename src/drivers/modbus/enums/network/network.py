import enum


class ModbusType(enum.Enum):
    RTU = 0
    TCP = 1


# The type of checksum to use to verify data integrity. This can be on of the followings.
class ModbusRtuParity(enum.Enum):
    O = 0
    E = 1
    N = 2
    Odd = 3
    Even = 4

# Bytesize
# The number of bits in a byte of serial data. This can be one of 5, 6, 7, or 8. This defaults to 8.

# Stopbits
# The number of bits sent after each character in a message to indicate the end of the byte. This defaults to 1.

# rtu_port = {
#     "/dev/ttyUSB0": "/dev/ttyUSB0",
#     "/dev/ttyUSB1": "/dev/ttyUSB1",
#     "/dev/ttyUSB2": "/dev/ttyUSB2",
#     "/dev/ttyUSB3": "/dev/ttyUSB3",
#     "/dev/ttyUSB4": "/dev/ttyUSB4",
# }
#
# rtu_parity = {
#     "even": "E",
#     "odd": "O",
#     "none": "N",
# }
#
# rtu_databits = {
#     "even": "E",
#     "odd": "O",
#     "none": "N",
# }
#
# rtu_baud_rate = {
#     "115200": 115200,
#     "57600": 57600,
#     "38400": 38400,
#     "19200": 19200,
#     "9600": 9600,
# }
