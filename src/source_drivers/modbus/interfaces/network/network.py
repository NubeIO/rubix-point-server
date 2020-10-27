import enum


class ModbusType(enum.Enum):
    RTU = 0
    TCP = 1


class ModbusRtuParity(enum.Enum):
    O = 0
    E = 1
    N = 2
    Odd = 3
    Even = 4
