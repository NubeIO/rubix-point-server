from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from src.modbus.interfaces.point.points import ModbusPointUtilsFuncs, ModbusPointUtils


def read_holding(client, reg_start, reg_length, _unit, data_type, endian):
    """
    read holding register
    :return:holding reg
    """
    reg_type = 'holding'
    read = client.read_holding_registers(reg_start, reg_length, unit=_unit)
    if _assertion(read, client, reg_type) == False:  # checking for errors
        bo_wo = _mod_point_data_endian(endian)
        byteorder = bo_wo['bo']
        wordorder = bo_wo['wo']
        data_type = _select_data_type(read, data_type, byteorder, wordorder)
        val = data_type
        return {'val': val, 'array': read.registers}


def _set_data_length(_val: str):
    """
    Sets the data length for the selected data type
    :return:holding reg
    """
    if ModbusPointUtilsFuncs.func_common_data_endian(_val):
        _type = ModbusPointUtils.mod_point_data_type
        int16 = _type['int16']
        uint16 = _type['uint16']
        int32 = _type['int16']
        uint32 = _type['uint32']
        _float = _type['float']
        _double = _type['double']
        if _val == int16 or _val == uint16:
            return 1
        if _val == int32 or _val == uint32 or _val == _float:
            return 2
        elif _val == _double:
            return 4


def _mod_point_data_endian(_val: str):
    """
    Sets byte order and endian order
    :return: array {'bo': bo, 'wo': wo}
    """
    if ModbusPointUtilsFuncs.func_common_data_endian(_val):
        if _val == ModbusPointUtils.mod_point_data_endian['LEB_BEW']:
            bo = Endian.Little
            wo = Endian.Big
            return {'bo': bo, 'wo': wo}
        if _val == ModbusPointUtils.mod_point_data_endian['LEB_LEW']:
            bo = Endian.Little
            wo = Endian.Little
            return {'bo': bo, 'wo': wo}
        if _val == ModbusPointUtils.mod_point_data_endian['BEB_LEW']:
            bo = Endian.Big
            wo = Endian.Little
            return {'bo': bo, 'wo': wo}
        if _val == ModbusPointUtils.mod_point_data_endian['BEB_BEW']:
            bo = Endian.Big
            wo = Endian.Big
            return {'bo': bo, 'wo': wo}


def _assertion(operation, client, reg_type):
    """
    :param operation: Client method. Checks whether data has been downloaded
    :return: Status False to OK or True.
    """
    # test that we are not an error
    if not operation.isError():
        pass
    else:
        print("connects to port: {}; Type Register: {}; Exception: {}".format(client.port,
                                                                              reg_type,
                                                                              operation, ))
    return operation.isError()


def _select_data_type(data, data_type, byteorder, wordorder):
    """
    Converts the data type int, int32, float and so on
    :param data: Log List Downloaded
    :return: data in the selected data type
    """
    decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=byteorder,
                                                 wordorder=wordorder)
    if data_type == 'int16':
        data = decoder.decode_16bit_int()
    if data_type == 'uint16':
        data = decoder.decode_16bit_uint()
    if data_type == 'int32':
        data = decoder.decode_32bit_int()
    if data_type == 'uint32':
        data = decoder.decode_32bit_uint()
    if data_type == 'float':
        data = decoder.decode_32bit_float()
    elif data_type == 'double':
        data = decoder.decode_32bit_float()

    return data
