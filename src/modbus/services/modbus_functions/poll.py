from src import ModbusPointStoreModel, TcpRegistry
from src.modbus.interfaces.point.points import ModbusPointType
from src.modbus.services.rtu_registry import RtuRegistry
from src.utils.data_funcs import DataHelpers
from src.modbus.services.modbus_functions.functions import read_holding


def poll_point(network, device, point, transport):
    connection = None
    if transport == "rtu":
        connection = RtuRegistry.get_rtu_connections().get(RtuRegistry.create_connection_key_by_network(network))
        if not connection:
            RtuRegistry.get_instance().add_network(network)
    if transport == "tcp":
        host = device.mod_tcp_device_ip
        port = device.mod_tcp_device_port
        connection = TcpRegistry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            TcpRegistry.get_instance().add_device(device)
    # TODO: whether it's functional or not, don't know how data we read
    reg = point.mod_point_reg
    mod_device_addr = device.mod_device_addr
    mod_point_reg_length = point.mod_point_reg_length
    mod_point_type = point.mod_point_type.name
    mod_point_data_type = point.mod_point_data_type.name
    mod_point_data_endian = point.mod_point_data_endian.name

    print(111)
    print(mod_point_data_type, mod_point_data_endian)

    try:
        val = None
        print({'mod_device_addr': mod_device_addr, 'reg': reg, 'mod_point_reg_length': mod_point_reg_length,
               'mod_point_type': mod_point_type})
        if mod_point_type == ModbusPointType.readCoils:
            val = connection.read_coils(reg, mod_point_reg_length, unit=mod_device_addr)
            val = val.bits[0]
            # array = val.bits
            val = DataHelpers.bool_to_int(val)
            print("read_coils", val)
        if mod_point_type == ModbusPointType.readHoldingRegisters.name:
            print(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                  mod_point_data_endian)
            read = read_holding(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                mod_point_data_endian)
            val = read['val']
            array = read['array']
            print("val", val, 'array', array)

        if val:
            print('done')
            # print("read_holding", val, 'array')
            # print("mod_point_type", mod_point_type, 'reg', reg, 'val', val,'array', array)
            ModbusPointStoreModel(mod_point_value=val, mod_point_uuid=point.mod_point_uuid).save_to_db()
    except Exception as e:
        print(f'Error: {str(e)}')
