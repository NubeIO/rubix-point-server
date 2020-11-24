import enum


class ModbusPointType(enum.Enum):
    READ_COILS = 1
    READ_DISCRETE_INPUTS = 2
    READ_HOLDING_REGISTERS = 3
    READ_INPUT_REGISTERS = 4
    WRITE_COIL = 5
    WRITE_REGISTER = 6
    WRITE_COILS = 15
    WRITE_REGISTERS = 16


class ModbusDataType(enum.Enum):
    RAW = 0
    INT16 = 1
    UINT16 = 2
    INT32 = 3
    UINT32 = 4
    FLOAT = 5
    DOUBLE = 6
    DIGITAL = 7


class ModbusDataEndian(enum.Enum):
    LEB_BEW = 1
    LEB_LEW = 2
    BEB_LEW = 3
    BEB_BEW = 4
