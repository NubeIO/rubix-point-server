from pymodbus.bit_write_message import WriteSingleCoilResponse, WriteMultipleCoilsResponse
from pymodbus.exceptions import ModbusIOException
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType, ModbusDataType, ModbusDataEndian
from src.source_drivers.modbus.services.modbus_functions.debug import modbus_debug_funcs
from src.source_drivers.modbus.services.modbus_functions.function_utils import _set_data_length, \
    _assertion, \
    _mod_point_data_endian, \
    _select_data_type, _builder_data_type


def read_analogue(client, reg_start: int, reg_length: int, _unit: int, data_type: ModbusDataType,
                  endian: ModbusDataEndian, func: ModbusPointType) -> (any, list):
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

    reg_length = _set_data_length(data_type,
                                  reg_length)
    if modbus_debug_funcs:
        print("MODBUS read_analogue",
              {"unit": _unit,
               "reg_start": reg_start,
               "reg_length": reg_length,
               "func": func
               })
    read = None

    if func == ModbusPointType.READ_HOLDING_REGISTERS:
        read = client.read_holding_registers(reg_start, reg_length, unit=_unit)
    elif func == ModbusPointType.READ_INPUT_REGISTERS:
        read = client.read_input_registers(reg_start, reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(read, client):  # checking for errors
        if modbus_debug_funcs:
            print("MODBUS _assertion", "read", read)

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


def read_digital(client, reg_start: int, reg_length: int, _unit: int, func: ModbusPointType) -> (any, list):
    """
    Read coil or digital input register
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param func: modbus function type
    :return: tuple (val: any, array: list)
    """

    if modbus_debug_funcs:
        print("MODBUS read_digital, check reg_length",
              {'reg_start': reg_start,
               'reg_length': reg_length,
               '_unit': _unit,
               'func': func})

    data_type = 'digital'
    reg_length = _set_data_length(data_type, reg_length)
    read = None

    if func == ModbusPointType.READ_COILS:
        read = client.read_coils(reg_start, reg_length, unit=_unit)
    elif func == ModbusPointType.READ_DISCRETE_INPUTS:
        read = client.read_discrete_inputs(reg_start, reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(read, client):  # checking for errors

        if modbus_debug_funcs:
            print("MODBUS DEBUG, func _assertion OK",
                  {'reg_start': reg_start,
                   'reg_length': reg_length,
                   '_unit': _unit,
                   'func': func})

        for ind in range(len(read.bits)):
            read.bits[ind] = int(read.bits[ind])
        val = read.bits[0]
        return val, read.bits[0:reg_length]
    else:
        if not isinstance(read, ModbusIOException):
            read = ModbusIOException(read)
        raise read


def write_digital(client, reg_start: int, reg_length: int, _unit: int, write_value: int, func: ModbusPointType) -> \
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

    if modbus_debug_funcs:
        print("MODBUS write_digital, check reg_length",
              {'reg_start': reg_start,
               'reg_length': reg_length,
               '_unit': _unit,
               'func': func})

    data_type = 'digital'
    reg_length = _set_data_length(data_type,
                                  reg_length)
    write = None
    if func == ModbusPointType.WRITE_COIL:
        write = client.write_coil(reg_start, write_value, unit=_unit)
    elif func == ModbusPointType.WRITE_COILS:
        write = client.write_coils(reg_start, [write_value]*reg_length, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(write, client):  # checking for errors

        if modbus_debug_funcs:
            print("MODBUS DEBUG _assertion OK",
                  {'reg_start': reg_start,
                   'reg_length': reg_length,
                   '_unit': _unit,
                   'func': func})
        if isinstance(write, WriteSingleCoilResponse):
            return int(write.value), [int(write.value)]
        else:
            return int(write_value), [int(write_value)]*reg_length
    else:
        if not isinstance(write, ModbusIOException):
            write = ModbusIOException(write)
        raise write


def write_analogue(client, reg_start: int, reg_length: int, _unit: int, data_type: ModbusDataType,
                   endian: ModbusDataEndian, write_value: float, func: ModbusPointType) -> (any, list):
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

    reg_length = _set_data_length(data_type,
                                  reg_length)

    if modbus_debug_funcs:
        print("MODBUS write_analogue, check reg_length",
              {'reg_start': reg_start,
               'reg_length': reg_length,
               '_unit': _unit,
               'func': func})

    byteorder, word_order = _mod_point_data_endian(endian)
    payload = _builder_data_type(write_value, data_type, byteorder, word_order)
    write = None
    if func == ModbusPointType.WRITE_REGISTER:
        write = client.write_register(reg_start, payload, unit=_unit)
    elif func == ModbusPointType.WRITE_REGISTERS:
        write = client.write_registers(reg_start, payload, unit=_unit)
    else:
        raise Exception('Invalid Modbus function code', func)

    if not _assertion(write, client):  # checking for errors

        if modbus_debug_funcs:
            print("MODBUS DEBUG _assertion OK",
                  {'reg_start': reg_start,
                   'reg_length': reg_length,
                   '_unit': _unit,
                   'func': func})

        return write_value, payload
    else:
        if not isinstance(write, ModbusIOException):
            write = ModbusIOException(write)
        raise write
