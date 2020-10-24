from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from src.modbus.interfaces.point.points import ModbusPointUtils, ModbusPointUtilsFuncs, ModbusDataEndian, ModbusDataType
from src.modbus.services.modbus_functions.debug import modbus_debug_funcs


def _set_data_length(data_type, reg_length):
    """
    Sets the data length for the selected data type
    :return:holding reg
    """
    if modbus_debug_funcs:
        print("MODBUS: in function  _set_data_length, check reg_length",
              {"data_type": data_type, "reg_length": reg_length})
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


def _mod_point_data_endian(_val):
    """
    Sets byte order and endian order
    LEB_BEW = 1
    LEB_LEW = 2
    BEB_LEW = 3
    BEB_BEW = 4
    :return: array {'bo': bo, 'wo': wo}
    """
    if _val == ModbusDataEndian.LEB_BEW:
        bo = Endian.Little
        wo = Endian.Big
        return {'bo': bo, 'wo': wo}
    if _val == ModbusDataEndian.LEB_LEW:
        bo = Endian.Little
        wo = Endian.Little
        return {'bo': bo, 'wo': wo}
    if _val == ModbusDataEndian.BEB_LEW:
        bo = Endian.Big
        wo = Endian.Little
        return {'bo': bo, 'wo': wo}
    if _val == ModbusDataEndian.BEB_BEW:
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


def _builder_data_type(payload, data_type, byteorder, word_order):
    """
    Converts the data type int, int32, float and so on
    :return: data in the selected data type
    """
    print(99999, payload, data_type, byteorder, word_order)
    builder = BinaryPayloadBuilder(byteorder=byteorder, wordorder=word_order)
    if data_type == ModbusDataType.INT16:
        builder.add_16bit_int(payload)
    if data_type == ModbusDataType.UINT16:
        builder.add_16bit_uint(payload)
    if data_type == ModbusDataType.INT32:
        builder.add_32bit_int(payload)
    if data_type == ModbusDataType.UINT32:
        builder.add_32bit_uint(payload)
    if data_type == ModbusDataType.FLOAT:
        builder.add_32bit_float(payload)
    elif data_type == ModbusDataType.DOUBLE:
        builder.add_64bit_float(payload)
    return builder.to_registers()

