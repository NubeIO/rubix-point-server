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
        host = device.tcp_ip
        port = device.tcp_port
        connection = TcpRegistry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            TcpRegistry.get_instance().add_device(device)
    # TODO: whether it's functional or not, don't know how data we read
    reg = point.reg
    device_addr = device.addr
    point_reg_length = point.reg_length
    point_type = point.type
    point_data_type = point.data_type
    point_data_endian = point.data_endian
    # debug
    if modbus_debug_poll:
        print("MODBUS:", {'network': network,
                          'device': device,
                          'transport': transport,
                          'device_addr': device_addr,
                          'reg': reg,
                          'point_reg_length': point_reg_length,
                          'point_type': point_type,
                          'point_data_type': point_data_type,
                          'point_data_endian': point_data_endian})

    try:
        val = None
        if point_type == ModbusPointType.READ_COILS:
            val = connection.read_coils(reg, point_reg_length, unit=device_addr)
            val = val.bits[0]
            val = DataHelpers.bool_to_int(val)
        if point_type == ModbusPointType.READ_HOLDING_REGISTERS:
            read = read_holding(connection, reg, point_reg_length, device_addr, point_data_type, point_data_endian)
            val = read['val']
            array = read['array']
            # debug
            if modbus_debug_poll:
                print("MODBUS:", {'type': ModbusPointType.READ_HOLDING_REGISTERS.name, "val": val, 'array': array})

        if val:
            # debug
            if modbus_debug_poll:
                print("MODBUS: READ/WRITE WAS DONE")
            ModbusPointStoreModel(value=val, point_uuid=point.uuid).save_to_db()
    except Exception as e:
        print(f'Error: {str(e)}')
