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

common_point_enable = {
    "enable": "enable",
    "disable": "disable",
}

# will only send if new value over MQTT
common_only_send_on_cov = {
    "enable": True,
    "disable": False,
}

common_registerDelay = 30

#
# def common_point_type(_val: str, _dict: dict) -> str:
#     for key, value in _dict.items():
#         if _val == value:
#             return _val
#         raise Exception("point type is not correct")
#
#
# def common_data_type(_val: str, _dict: dict) -> str:
#     for key, value in _dict.items():
#         if _val == value:
#             return _val
#         raise Exception("data type is not correct")
#
#
# def func_common_data_endian(_val: str, _dict: dict) -> str:
#     for key, value in _dict.items():
#         if _val == value:
#             return _val
#         raise Exception("endian is not correct")
#
#
# val = "LEB_BEW1"
# test = func_common_data_endian(val, common_data_endian)
# print(test)
