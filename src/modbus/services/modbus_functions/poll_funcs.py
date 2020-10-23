from src.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.modbus.services.modbus_functions.functions import read_digital, write_digital
from src.utils.data_funcs import DataHelpers


def read_coils_func(mod_point_type, connection, reg, mod_point_reg_length, mod_device_addr):
    read = read_digital(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type)
    single = read['val']
    array = read['array']
    val = DataHelpers.bool_to_int(single)
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val


def write_coil_func(mod_point_type, connection, reg, mod_point_reg_length, mod_device_addr, write_value):
    read = write_digital(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_type, write_value)
    single = read['val']
    array = read['array']
    val = DataHelpers.bool_to_int(single)
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'type': mod_point_type, "val": val, 'array': array})
    return val
