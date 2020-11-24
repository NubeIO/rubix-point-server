import logging

from src.loggers import modbus_debug
from src.source_drivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue

logger = logging.getLogger(modbus_debug)


def read_digital_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type):
    val, array = read_digital(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type)
    debug_log(mod_point_type, array, val)
    return val, array


def write_coil_handle(connection, reg, mod_point_reg_length, mod_device_addr, write_value, mod_point_type):
    val, array = write_digital(connection, reg, mod_point_reg_length, mod_device_addr, write_value, mod_point_type)
    debug_log(mod_point_type, array, val)
    return val, array


def read_analog_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                       mod_point_data_endian, mod_point_type):
    val, array = read_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                               mod_point_data_endian, mod_point_type)
    debug_log(mod_point_type, array, val)
    return val, array


def write_holding_registers_handle(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                   mod_point_data_endian, write_value, mod_point_type):
    val, array = write_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                mod_point_data_endian, write_value, mod_point_type)
    debug_log(mod_point_type, array, val)
    return val, array


def debug_log(mod_point_type, array, val):
    logger.debug(f'Returned value: {{"type": {mod_point_type}, "array": {array}, "val": {val}}}')
