import enum


class ModbusFC(enum.Enum):
    readCoils = 'readCoils'
    readDiscreteInputs = 'readDiscreteInputs',
    readHoldingRegisters = 'readHoldingRegisters',
    readInputRegisters = 'readInputRegisters',
    writeCoil = 'writeCoil',
    writeRegister = 'writeRegister',
    writeCoils = 'writeCoils',
    writeRegisters = 'writeRegisters'

class ModbusPointUtils:
    common_point_type = {
        "readCoils": "readCoils",
        "readDiscreteInputs": "readDiscreteInputs",
        "readHoldingRegisters": "readHoldingRegisters",
        "readInputRegisters": "readInputRegisters",
        "writeCoil": "writeCoil",
        "writeRegister": "writeRegister",
        "writeCoils": "writeCoils",
        "writeRegisters": "writeRegisters"
    }
    common_data_type = {
        "int16": "int16",
        "uint16": "uint16",
        "int32": "int32",
        "uint32": "uint32",
        "float": "float",
        "double": "double",
    }
    common_data_endian = {
        "LEB_BEW": "LEB_BEW",
        "LEB_LEW": "LEB_LEW",
        "BEB_LEW": "BEB_LEW",
        "BEB_BEW": "BEB_BEW"
    }


class ModbusPointUtilsFuncs:

    @classmethod
    def common_point_type(cls, _val: str) -> str:
        for key, value in ModbusPointUtils.common_point_type.items():
            if _val == value:
                return _val
            raise Exception("point type is not correct")

    @classmethod
    def common_data_type(cls, _val: str) -> str:

        for key, value in ModbusPointUtils.common_data_type.items():
            if _val == value:
                return _val
            raise Exception("data type is not correct")

    @classmethod
    def func_common_data_endian(cls, _val: str) -> str:

        for key, value in ModbusPointUtils.common_data_endian.items():
            if _val == value:
                return _val
            raise Exception("endian is not correct")