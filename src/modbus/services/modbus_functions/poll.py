from src import ModbusPointStoreModel, TcpRegistry
from src.modbus.interfaces.point.points import ModbusPointType
from src.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.modbus.services.rtu_registry import RtuRegistry
from src.utils.data_funcs import DataHelpers
from src.modbus.services.modbus_functions.functions import read_analogue, read_digital


def poll_point(network, device, point, transport) -> None:
    """
    Main modbus polling loop
    :param network: modbus network class
    :param device: modbus device class
    :param point: modbus point class
    :param transport: modbus transport as in TCP or RTU
    :return: None
    """
    """
    DEBUG
    """
    if modbus_debug_poll:
        print('MODBUS DEBUG: main looping function poll_point')
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
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("MODBUS DEBUG:", {'network': network,
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
        read_coils = ModbusPointType.readCoils.name
        read_holding_registers = ModbusPointType.readHoldingRegisters.name
        read_input_registers = ModbusPointType.readInputRegisters.name
        read_discrete_input = ModbusPointType.readDiscreteInputs.name
        write_coil = ModbusPointType.writeCoil.name
        write_register = ModbusPointType.writeRegister.name
        write_coils = ModbusPointType.writeCoils.name
        write_registers = ModbusPointType.writeRegisters.name
        """
        read_coils
        """
        if mod_point_type == read_coils:
            func = read_coils
            read = read_digital(connection, reg, mod_point_reg_length, mod_device_addr, func)
            single = read['val']
            array = read['array']
            val = DataHelpers.bool_to_int(single)
            """
            DEBUG
            """
            if modbus_debug_poll:
                print("MODBUS DEBUG:", {'type': read_coils, "val": val, 'array': array})
        """
        read_holding_registers
        """
        if mod_point_type == read_input_registers:
            func = read_input_registers
            read = read_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                 mod_point_data_endian, func)
            val = read['val']
            array = read['array']
            """
            DEBUG
            """
            if modbus_debug_poll:
                print("MODBUS DEBUG:", {'type': read_holding_registers, "val": val, 'array': array})
        """
        Save modbus data in database
        """
        if mod_point_type == read_holding_registers:
            func = read_holding_registers
            read = read_analogue(connection, reg, mod_point_reg_length, mod_device_addr, mod_point_data_type,
                                 mod_point_data_endian, func)
            val = read['val']
            array = read['array']
            """
            DEBUG
            """
            if modbus_debug_poll:
                print("MODBUS DEBUG:", {'type': read_holding_registers, "val": val, 'array': array})
        """
        Save modbus data in database
        """
        if val:
            # TODO add in last poll timestamp, point write/fault status and modbus array to db
            """
            DEBUG
            """
            if modbus_debug_poll:
                print("MODBUS DEBUG:  READ/WRITE WAS DONE", 'TRANSPORT TYPE= ', transport)
            # ModbusPointStoreModel(mod_point_value=val, mod_point_uuid=point.mod_point_uuid).save_to_db()
    except Exception as e:
        print(f'MODBUS ERROR: in poll main function {str(e)}')
