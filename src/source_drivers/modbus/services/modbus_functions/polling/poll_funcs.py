from src.source_drivers.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.source_drivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue


def read_digital_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type):
    val, array = read_digital(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type)

    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val, array


def write_coil_handle(connection, reg, mod_point_reg_length, mod_device_addr, write_value, mod_point_type):
    val, array = write_digital(connection, reg, mod_point_reg_length, mod_device_addr, write_value, mod_point_type)

    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val, array


def read_analog_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                       mod_point_data_endian, mod_point_type):
    val, array = read_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                               mod_point_data_endian, mod_point_type)

    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val, array


def write_holding_registers_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                   mod_point_data_endian, write_value, mod_point_type):
    if modbus_debug_poll:
        print("MODBUS DEBUG: try and read a register", {'type': mod_point_type})
    val, array = write_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                mod_point_data_endian, write_value, mod_point_type)

    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val, array
