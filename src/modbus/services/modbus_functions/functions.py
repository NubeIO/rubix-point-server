from src.modbus.interfaces.point.points import ModbusPointType
from src.modbus.services.modbus_functions.debug import modbus_debug_funcs
from src.modbus.services.modbus_functions.function_utils import _set_data_length, \
    _assertion, \
    _mod_point_data_endian, \
    _select_data_type


def read_analogue(client, reg_start: int, reg_length: int, _unit: int, data_type, endian, func) -> dict:
    """
    Read holding or input register
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param data_type: data type int, float
    :param endian: data type endian
    :param func: modbus function type
    :return: dict
    """
    read_holding_registers = ModbusPointType.READ_HOLDING_REGISTERS
    read_input_registers = ModbusPointType.READ_DISCRETE_INPUTS
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_analogue, check reg_length")

    """
    check that user if for example wants data type of float that the reg_length is > = 2
    """
    reg_length = _set_data_length(data_type,
                                  reg_length)
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_analogue, check reg_length result then do modbus read",
              {"unit": _unit,
               "reg_start": reg_start,
               "reg_length": reg_length,
               "func": func,
               "read_holding_registers": read_holding_registers,
               "read_input_registers": read_input_registers})
    read = None
    reg_type = None
    """
    Select which type of modbus read to do
    """
    if func == read_holding_registers:
        read = client.read_holding_registers(reg_start, reg_length, unit=1)
        reg_type = 'holding'
        """
        DEBUG
        """
        if modbus_debug_funcs:
            print("MODBUS DO READ HOLDING", {'read': read})
    if func == read_input_registers:
        read = client.read_input_registers(reg_start, reg_length, unit=_unit)
        reg_type = 'input'
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_analogue, do modbus read", "read", read, "reg_type", reg_type)
    if not _assertion(read, client, reg_type):  # checking for errors
        if modbus_debug_funcs:
            print("MODBUS _assertion, after modbus read", "read", read, "reg_type", reg_type)
        """
        set up for word and byte order
        """
        bo_wo = _mod_point_data_endian(endian)
        byteorder = bo_wo['bo']
        word_order = bo_wo['wo']
        """
        Converts the data type int, int32, float and so on
        """
        data_type = _select_data_type(read, data_type, byteorder, word_order)
        val = data_type
        return {'val': val, 'array': read.registers}


def read_digital(client, reg_start: int, reg_length: int, _unit: int, func) -> dict:
    """
    Read coil or digital input register
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param func: modbus function type
    :return: dict
    """
    read_coils = ModbusPointType.READ_COILS
    read_discrete_input = ModbusPointType.READ_DISCRETE_INPUTS
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, check reg_length",
              {'reg_start': reg_start,
               'reg_length': reg_length,
               '_unit': _unit,
               'func': func})

    """
    check that user if for example wants data type of float that the reg_length is > = 2
    """
    data_type = 'digital'
    reg_length = _set_data_length(data_type,
                                  reg_length)
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, check reg_length result then do modbus read", "reg_length",
              reg_length)
    read = None
    reg_type = None
    """
    Select which type of modbus read to do
    """
    if func == read_coils:
        read = client.read_coils(reg_start, reg_length, unit=_unit)
        reg_type = 'coil'
    if func == read_discrete_input:
        read = client.read_discrete_inputs(reg_start, reg_length, unit=_unit)
        reg_type = 'disc_input'
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, do modbus read", "read", read, "reg_type", reg_type)
    if not _assertion(read, client, reg_type):  # checking for errors
        """
        DEBUG
        """
        if modbus_debug_funcs:
            print("MODBUS DEBUG, func _assertion, check data is valid (if in here modbus read was good)",
                  {'reg_start': reg_start,
                   'reg_length': reg_length,
                   '_unit': _unit,
                   'func': func})

        val = read.bits[0]
        array = read.bits
        return {'val': val, 'array': array}


def write_digital(client, reg_start: int, reg_length: int, _unit: int, func, write_value: int) -> dict:
    """
    Write coil
    :param client: modbus client
    :param reg_start: modbus client
    :param reg_length: modbus client
    :param _unit: modbus address as an int
    :param func: modbus function type
    :return: dict
    """
    write_coil = ModbusPointType.WRITE_COIL
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, check reg_length",
              {'reg_start': reg_start,
               'reg_length': reg_length,
               '_unit': _unit,
               'func': func})

    """
    check that user if for example wants data type of float that the reg_length is > = 2
    """
    data_type = 'digital'
    reg_length = _set_data_length(data_type,
                                  reg_length)
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, check reg_length result then do modbus read", "reg_length",
              reg_length)
    read = None
    reg_type = None
    """
    Select which type of modbus read to do
    """
    if func == write_coil:
        print(1231234234, 'write_value', write_value)
        read = client.write_coil(reg_start, write_value, unit=_unit)
        print(1231234234)
        print(read)
        reg_type = 'coil'
    """
    DEBUG
    """
    if modbus_debug_funcs:
        print("MODBUS read_digital, do modbus read", "read", read, "reg_type", reg_type)
    if not _assertion(read, client, reg_type):  # checking for errors
        """
        DEBUG
        """
        if modbus_debug_funcs:
            print("MODBUS DEBUG, func _assertion, check data is valid (if in here modbus read was good)",
                  {'reg_start': reg_start,
                   'reg_length': reg_length,
                   '_unit': _unit,
                   'func': func})

        # val = read.bits[0]
        # array = read.bits
        return {'val': read, 'array': read}
