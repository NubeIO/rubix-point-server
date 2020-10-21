from src import ModbusPointStoreModel, TcpRegistry
from src.modbus.interfaces.point.points import ModbusPointType
from src.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.modbus.services.rtu_registry import RtuRegistry
from src.utils.data_funcs import DataHelpers
from src.modbus.services.modbus_functions.functions import read_holding


def poll_point(network, device, point, transport):
    if modbus_debug_poll:
        print('MODBUS: main looping function poll_point')
    connection = None
    if transport == "rtu":
        connection = RtuRegistry.get_rtu_connections().get(RtuRegistry.create_connection_key_by_network(network))
        if not connection:
            RtuRegistry.get_instance().add_network(network)
    if transport == "tcp":
        host = device.tcp_device_ip
        port = device.tcp_device_port
        connection = TcpRegistry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            TcpRegistry.get_instance().add_device(device)
    # TODO: whether it's functional or not, don't know how data we read
    reg = point.mod_point_reg
    mod_device_addr = device.addr
    mod_point_reg_length = point.mod_point_reg_length
    mod_point_type = point.mod_point_type.name
    mod_point_data_type = point.mod_point_data_type.name
    mod_point_data_endian = point.mod_point_data_endian.name
    # debug
    if modbus_debug_poll:
        print("MODBUS:", {'network': network,
                          'device': device,
                          'transport': transport,
                          'mod_device_addr': mod_device_addr,
                          'reg': reg,
                          'mod_point_reg_length': mod_point_reg_length,
                          'mod_point_type': mod_point_type,
                          'mod_point_data_type': mod_point_data_type,
                          'mod_point_data_endian': mod_point_data_endian})

    try:
        val = None
        if mod_point_type == ModbusPointType.readCoils:
            val = connection.read_coils(reg, mod_point_reg_length, unit=mod_device_addr)
            val = val.bits[0]
            val = DataHelpers.bool_to_int(val)
        if mod_point_type == ModbusPointType.readHoldingRegisters.name:
            read = read_holding(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                mod_point_data_endian)
            val = read['val']
            array = read['array']
            # debug
            if modbus_debug_poll:
                print("MODBUS:", {'type': ModbusPointType.readHoldingRegisters.name, "val": val, 'array': array})

        if val:
            # debug
            if modbus_debug_poll: print("MODBUS: READ/WRITE WAS DONE")
            ModbusPointStoreModel(mod_point_value=val, mod_point_uuid=point.mod_point_uuid).save_to_db()
    except Exception as e:
        print(f'Error: {str(e)}')
