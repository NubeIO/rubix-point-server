from src.modbus.interfaces.point.points import ModbusPointUtils
from src.modbus.services.modbus_functions.debug import modbus_debug_funcs


def _set_data_length(data_type, reg_length):
    """
    Sets the data length for the selected data type
    :return:holding reg
    """
    if modbus_debug_funcs: print("MODBUS: in function  _set_data_length, check reg_length", data_type, reg_length)
    _val = data_type
    length = reg_length

    if True: #TODO add a check for data type
        _type = ModbusPointUtils.mod_point_data_type
        _int16 = _type['int16']
        _uint16 = _type['uint16']
        _int32 = _type['int16']
        _uint32 = _type['uint32']
        _float = _type['float']
        _double = _type['double']
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

