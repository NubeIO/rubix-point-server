from typing import List

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

from src.drivers.modbus.enums.point.points import ModbusDataEndian, ModbusDataType
from src.drivers.modbus.models.point import ModbusPointModel
from src.models.point.priority_array import PriorityArrayModel


def _set_data_length(data_type: ModbusDataType, reg_length: int) -> int:
    """
    Sets the data length for the selected data type
    :return: register length
    """

    if data_type == ModbusDataType.RAW:
        return reg_length
    elif data_type == ModbusDataType.DIGITAL or data_type == ModbusDataType.INT16 or data_type == ModbusDataType.UINT16:
        return reg_length if reg_length >= 1 else 1
    elif data_type == ModbusDataType.INT32 or data_type == ModbusDataType.UINT32 or data_type == ModbusDataType.FLOAT:
        return reg_length if reg_length >= 2 else 2
    elif data_type == ModbusDataType.DOUBLE:
        return reg_length if reg_length >= 4 else 4


def _mod_point_data_endian(_val: ModbusDataEndian) -> (Endian, Endian):
    """
    Sets byte order and endian order
    :return: tuple (bo: Endian, wo: Endian)
    """
    bo = None
    wo = None
    if _val == ModbusDataEndian.LEB_BEW:
        bo = Endian.Little
        wo = Endian.Big
    elif _val == ModbusDataEndian.LEB_LEW:
        bo = Endian.Little
        wo = Endian.Little
    elif _val == ModbusDataEndian.BEB_LEW:
        bo = Endian.Big
        wo = Endian.Little
    elif _val == ModbusDataEndian.BEB_BEW:
        bo = Endian.Big
        wo = Endian.Big
    return bo, wo


def _assertion(operation):
    """
    :param operation: Client method. Checks whether data has been downloaded
    :return: Status False to OK or True.
    """
    # test that we are not an error
    if not operation.isError():
        pass
    return operation.isError()


def convert_to_data_type(data, data_type: ModbusDataType, byteorder: Endian, word_order: Endian):
    """
    Converts the data to int, int32, float and so on
    :return: value in the selected data type
    """
    decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=byteorder,
                                                 wordorder=word_order)
    value = None
    if data_type == ModbusDataType.INT16:
        value = decoder.decode_16bit_int()
    if data_type == ModbusDataType.UINT16:
        value = decoder.decode_16bit_uint()
    if data_type == ModbusDataType.INT32:
        value = decoder.decode_32bit_int()
    if data_type == ModbusDataType.UINT32:
        value = decoder.decode_32bit_uint()
    if data_type == ModbusDataType.FLOAT:
        value = decoder.decode_32bit_float()
    elif data_type == ModbusDataType.DOUBLE:
        value = decoder.decode_16bit_float()
    return value


def _builder_data_type(payload, data_type: ModbusDataType, byteorder: Endian, word_order: Endian):
    """
    Converts the data type int, int32, float and so on
    :return: data in the selected data type
    """
    builder = BinaryPayloadBuilder(byteorder=byteorder, wordorder=word_order)
    if data_type == ModbusDataType.INT16:
        builder.add_16bit_int(int(payload))
    if data_type == ModbusDataType.UINT16:
        builder.add_16bit_uint(int(payload))
    if data_type == ModbusDataType.INT32:
        builder.add_32bit_int(int(payload))
    if data_type == ModbusDataType.UINT32:
        builder.add_32bit_uint(int(payload))
    if data_type == ModbusDataType.FLOAT:
        builder.add_32bit_float(payload)
    elif data_type == ModbusDataType.DOUBLE:
        builder.add_64bit_float(payload)
    return builder.to_registers()


def pack_point_write_registers(point_list: List[ModbusPointModel]):
    final_payload = []
    for point in point_list:
        byteorder, word_order = _mod_point_data_endian(point.data_endian)
        write_value: float = PriorityArrayModel.get_highest_priority_value_from_dict(point.priority_array_write) or 0
        final_payload.extend(_builder_data_type(write_value, point.data_type, byteorder, word_order))
    return final_payload
