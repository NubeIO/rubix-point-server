from src.sourceDrivers.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.sourceDrivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, \
    write_analogue
from src.utils.data_funcs import DataHelpers


def read_coils_handle(connection, reg, mod_point_reg_length,
                      mod_device_addr, mod_point_type):
    read = read_digital(connection, reg, mod_point_reg_length,
                        mod_device_addr, mod_point_type)
    single = read['val']
    array = read['array']
    val = DataHelpers.bool_to_int(single)
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val


def write_coil_handle(connection, reg, mod_point_reg_length,
                      mod_device_addr, write_value, mod_point_type):
    read = write_digital(connection, reg, mod_point_reg_length,
                         mod_device_addr, write_value, mod_point_type)
    single = read['val']
    array = read['array']
    val = DataHelpers.bool_to_int(single)
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val


def read_input_registers_handle(connection, reg, mod_point_reg_length,
                                mod_device_addr, mod_point_data_type,
                                mod_point_data_endian, mod_point_type):
    read = read_analogue(connection, reg, mod_point_reg_length,
                         mod_device_addr, mod_point_data_type,
                         mod_point_data_endian, mod_point_type)
    val = read['val']
    array = read['array']
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val


def read_holding_registers_handle(connection, reg, mod_point_reg_length,
                                  mod_device_addr, mod_point_data_type,
                                  mod_point_data_endian, mod_point_type):
    if modbus_debug_poll:
        print("MODBUS DEBUG: inside read_holding_registers_handle try and read", {'type': mod_point_type})
    read = read_analogue(connection, reg, mod_point_reg_length,
                         mod_device_addr, mod_point_data_type,
                         mod_point_data_endian, mod_point_type)
    val = read['val']
    array = read['array']
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG: inside read_holding_registers_handle AFTER read",
              {'type': mod_point_type, "val": val, 'array': array})
    return val


def write_registers_handle(connection, reg, mod_point_reg_length,
                           mod_device_addr, mod_point_data_type,
                           mod_point_data_endian, write_value, mod_point_type):
    if modbus_debug_poll:
        print("MODBUS DEBUG: try and read a register", {'type': mod_point_type})
    read = write_analogue(connection, reg, mod_point_reg_length,
                          mod_device_addr, mod_point_data_type,
                          mod_point_data_endian, write_value, mod_point_type)
    val = read['val']
    array = read['array']
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val
