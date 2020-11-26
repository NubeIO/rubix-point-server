import logging

from pymodbus.bit_write_message import WriteSingleCoilResponse
from pymodbus.exceptions import ModbusIOException

from src.loggers import modbus_debug
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian
from src.source_drivers.modbus.services.modbus_functions.function_utils import _set_data_length, _assertion, \
    _mod_point_data_endian, _select_data_type, _builder_data_type

logger = logging.getLogger(modbus_debug)


def read_analogue(client, reg_start: int, reg_length: int, _unit: int, data_type: ModbusDataType,
                  endian: ModbusDataEndian, func: ModbusFunctionCode) -> (any, list):
    """
    Read holding or input register
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param data_type: data type int, float
    :param endian: data type endian
    :param func: modbus function type
    :return: tuple (val: any, array: list)
    """
    debug_log('read_analogue', _unit, func, reg_length, reg_start)
    reg_length = _set_data_length(data_type, reg_length)
    if func == ModbusFunctionCode.READ_HOLDING_REGISTERS:
        read = client.read_holding_registers(reg_start, reg_length, unit=_unit)
    elif func == ModbusFunctionCode.READ_INPUT_REGISTERS:
        read = client.read_input_registers(reg_start, reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(read):  # checking for errors
        assertion_ok_debug_log(_unit, func, reg_length, reg_start)
        if data_type is not ModbusDataType.RAW:
            byteorder, word_order = _mod_point_data_endian(endian)
            val = _select_data_type(read, data_type, byteorder, word_order)
        else:
            val = read.registers[0]  # first register
        return val, read.registers
    else:
        if not isinstance(read, ModbusIOException):
            read = ModbusIOException(read)
        raise read


def read_digital(client, reg_start: int, reg_length: int, _unit: int, func: ModbusFunctionCode) -> (any, list):
    """
    Read coil or digital input register
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param func: modbus function type
    :return: tuple (val: any, array: list)
    """
    debug_log('read_digital', _unit, func, reg_length, reg_start)
    data_type = 'digital'
    reg_length = _set_data_length(data_type, reg_length)
    if func == ModbusFunctionCode.READ_COILS:
        read = client.read_coils(reg_start, reg_length, unit=_unit)
    elif func == ModbusFunctionCode.READ_DISCRETE_INPUTS:
        read = client.read_discrete_inputs(reg_start, reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(read):  # checking for errors
        assertion_ok_debug_log(_unit, func, reg_length, reg_start)
        for ind in range(len(read.bits)):
            read.bits[ind] = int(read.bits[ind])
        val = read.bits[0]
        return val, read.bits[0:reg_length]
    else:
        if not isinstance(read, ModbusIOException):
            read = ModbusIOException(read)
        raise read


def write_digital(client, reg_start: int, reg_length: int, _unit: int, write_value: int, func: ModbusFunctionCode) -> \
        (any, list):
    """
    Write coil
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param write_value: value to write to coil
    :param func: modbus function type
    :return: tuple (val: any, array: list)
    """
    debug_log('write_digital', _unit, func, reg_length, reg_start)
    data_type = 'digital'
    reg_length = _set_data_length(data_type, reg_length)
    if func == ModbusFunctionCode.WRITE_COIL:
        write = client.write_coil(reg_start, write_value, unit=_unit)
    elif func == ModbusFunctionCode.WRITE_COILS:
        write = client.write_coils(reg_start, [write_value] * reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(write):  # checking for errors
        assertion_ok_debug_log(_unit, func, reg_length, reg_start)
        if isinstance(write, WriteSingleCoilResponse):
            return int(write.value), [int(write.value)]
        else:
            return int(write_value), [int(write_value)] * reg_length
    else:
        if not isinstance(write, ModbusIOException):
            write = ModbusIOException(write)
        raise write


def write_analogue(client, reg_start: int, reg_length: int, _unit: int, data_type: ModbusDataType,
                   endian: ModbusDataEndian, write_value: float, func: ModbusFunctionCode) -> (any, list):
    """
    Write holding reg
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param data_type: data type int, float
    :param endian: data type endian
    :param write_value: value to write to register
    :param func: modbus function type
    :return: tuple (val: any, array: list)
    """
    debug_log('write_analogue', _unit, func, reg_length, reg_start)
    reg_length = _set_data_length(data_type, reg_length)
    byteorder, word_order = _mod_point_data_endian(endian)
    payload = _builder_data_type(write_value, data_type, byteorder, word_order)
    if func == ModbusFunctionCode.WRITE_REGISTER:
        write = client.write_register(reg_start, payload, unit=_unit)
    elif func == ModbusFunctionCode.WRITE_REGISTERS:
        write = client.write_registers(reg_start, payload, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(write):  # checking for errors
        assertion_ok_debug_log(_unit, func, reg_length, reg_start)
        return write_value, payload
    else:
        if not isinstance(write, ModbusIOException):
            write = ModbusIOException(write)
        raise write


def debug_log(name, _unit, func, reg_length, reg_start):
    logger.debug(
        f'{name}, check reg_length {{"reg_start": {reg_start}, "reg_length": {reg_length}, "_unit:" {_unit}}}, "func": {func}}}')


def assertion_ok_debug_log(_unit, func, reg_length, reg_start):
    logger.debug(
        f'_assertion OK {{"reg_start": {reg_start}, "reg_length": {reg_length}, "unit:" {_unit}}}, "func": {func}}}')
