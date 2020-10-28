import enum


class ModbusType(enum.Enum):
    RTU = 0
    TCP = 1


# Parity
# The type of checksum to use to verify data integrity. This can be on of the following
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
