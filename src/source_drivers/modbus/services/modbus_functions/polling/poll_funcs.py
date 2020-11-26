import logging

from src.loggers import modbus_debug
from src.source_drivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue

logger = logging.getLogger(modbus_debug)


def read_digital_handle(connection, reg, point_reg_length, device_addr, point_fc):
    val, array = read_digital(connection, reg, point_reg_length, device_addr, point_fc)
    debug_log(point_fc, array, val)
    return val, array


def write_coil_handle(connection, reg, point_reg_length, device_addr, write_value, point_fc):
    val, array = write_digital(connection, reg, point_reg_length, device_addr, write_value, point_fc)
    debug_log(point_fc, array, val)
    return val, array


def read_analog_handle(connection, reg, point_reg_length, device_addr, point_data_type,
                       point_data_endian, point_fc):
    val, array = read_analogue(connection, reg, point_reg_length, device_addr, point_data_type,
                               point_data_endian, point_fc)
    debug_log(point_fc, array, val)
    return val, array


def write_holding_registers_handle(connection, reg, point_reg_length, device_addr, point_data_type,
                                   point_data_endian, write_value, point_fc):
    val, array = write_analogue(connection, reg, point_reg_length, device_addr, point_data_type,
                                point_data_endian, write_value, point_fc)
    debug_log(point_fc, array, val)
    return val, array


def debug_log(point_fc, array, val):
    logger.debug(f'Returned value: {{"FC": {point_fc}, "array": {array}, "val": {val}}}')
