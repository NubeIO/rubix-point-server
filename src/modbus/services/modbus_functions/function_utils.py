from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from src.modbus.interfaces.point.points import ModbusPointUtils, ModbusPointUtilsFuncs
from src.modbus.services.modbus_functions.debug import modbus_debug_funcs


def _set_data_length(data_type, reg_length):
    """
    Sets the data length for the selected data type
    :return:holding reg
    """
    if modbus_debug_funcs: print("MODBUS: in function  _set_data_length, check reg_length", data_type, reg_length)
    _val = data_type
    length = reg_length

    if True:  # TODO add a check for data type
        _type = ModbusPointUtils.mod_point_data_type
        _digital = _type['digital']
        _int16 = _type['int16']
        _uint16 = _type['uint16']
        _int32 = _type['int16']
        _uint32 = _type['uint32']
        _float = _type['float']
        _double = _type['double']
        if _digital:
            if reg_length < 1:
                return 1
            else:
                return length
        if _val == _int16 or _val == _uint16:
            if reg_length < 1:
                return 1
            else:
                return length
        if _val == _int32 or _val == _uint32 or _val == _float:
            if reg_length < 2:
                return 2
            else:
                return length
        elif _val == _double:
            if reg_length < 4:
                return 4
            else:
                return length


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


def _select_data_type(data, data_type, byteorder, word_order):
    """
    Converts the data type int, int32, float and so on
    :param data: Log List Downloaded
    :return: data in the selected data type
    """
    decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=byteorder,
                                                 wordorder=word_order)
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
