import numbers
from src import TcpRegistry, ModbusPointStoreModel
from src.modbus.interfaces.network.network import ModbusType
from src.modbus.interfaces.point.points import ModbusPointType
from src.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.modbus.services.modbus_functions.polling.poll_funcs import read_input_registers_handle, \
    read_holding_registers_handle, \
    write_coil_handle, \
    read_coils_handle, write_registers_handle
from src.modbus.services.rtu_registry import RtuRegistry


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
    if transport == ModbusType.RTU:
        connection = RtuRegistry.get_rtu_connections().get(RtuRegistry.create_connection_key_by_network(network))
        if not connection:
            RtuRegistry.get_instance().add_network(network)
    if transport == ModbusType.TCP:
        host = device.tcp_ip
        port = device.tcp_port
        connection = TcpRegistry.get_tcp_connections().get(TcpRegistry.create_connection_key(host, port))
        if not connection:
            TcpRegistry.get_instance().add_device(device)
    # TODO: whether it's functional or not, don't know how data we read

    mod_device_addr = device.addr
    reg = point.reg
    mod_point_reg_length = point.reg_length
    mod_point_type = point.type
    mod_point_data_type = point.data_type
    mod_point_data_endian = point.data_endian

    write_value = point.write_value
    read_coils = ModbusPointType.READ_COILS
    write_coil = ModbusPointType.WRITE_COIL
    read_holding_registers = ModbusPointType.READ_HOLDING_REGISTERS
    read_input_registers = ModbusPointType.READ_DISCRETE_INPUTS
    write_registers = ModbusPointType.WRITE_REGISTERS
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
                                'mod_point_data_endian': mod_point_data_endian,
                                'read_coils': read_coils,
                                'read_holding_registers': read_holding_registers,
                                'read_input_registers': read_input_registers,
                                })

    fault = False
    fault_message = ""
    point_store = None
    try:
        val = None
        array = ""
        """
        read_coils
        """
        if mod_point_type == read_coils:
            val = read_coils_handle(connection,
                                    reg,
                                    mod_point_reg_length,
                                    mod_device_addr,
                                    mod_point_type)
        """
        write_coils
        """
        if mod_point_type == write_coil:
            val = write_coil_handle(connection, reg,
                                    mod_point_reg_length,
                                    mod_device_addr,
                                    write_value,
                                    mod_point_type)
        """
        read_input_registers
        """
        if mod_point_type == read_input_registers:
            val = read_input_registers_handle(connection,
                                              reg,
                                              mod_point_reg_length,
                                              mod_device_addr,
                                              mod_point_data_type,
                                              mod_point_data_endian,
                                              mod_point_type)
        """
        read_holding_registers
        """
        if mod_point_type == read_holding_registers:
            val = read_holding_registers_handle(connection,
                                                reg,
                                                mod_point_reg_length,
                                                mod_device_addr,
                                                mod_point_data_type,
                                                mod_point_data_endian,
                                                mod_point_type)
        """
        read_holding_registers 
        """
        if mod_point_type == read_holding_registers:
            val = read_holding_registers_handle(connection,
                                                reg,
                                                mod_point_reg_length,
                                                mod_device_addr,
                                                mod_point_data_type,
                                                mod_point_data_endian,
                                                mod_point_type)
        """
        write_registers write_registers
        """
        if mod_point_type == write_registers:
            val = write_registers_handle(connection,
                                         reg,
                                         mod_point_reg_length,
                                         mod_device_addr,
                                         mod_point_data_type,
                                         mod_point_data_endian,
                                         write_value,
                                         mod_point_type)

        """
        Save modbus data in database
        """
        if modbus_debug_poll:
            print("MODBUS DEBUG: READ/WRITE WAS DONE", 'TRANSPORT TYPE =', transport)
        if isinstance(val, numbers.Number):
            point_store = ModbusPointStoreModel(value=val, value_array=str(array), point_uuid=point.uuid)
        else:
            fault = True
            fault_message = "Got not numeric value"
    except Exception as e:
        print(f'MODBUS ERROR: in poll main function {str(e)}')
        fault = True
        fault_message = str(e)

    if not point_store:
        last_valid_row = ModbusPointStoreModel.find_last_valid_row(point.uuid)
        if last_valid_row:
            point_store = ModbusPointStoreModel(value=last_valid_row.value, value_array=last_valid_row.value_array,
                                                fault=fault, fault_message=fault_message, point_uuid=point.uuid)
        else:
            point_store = ModbusPointStoreModel(value=0, fault=fault, fault_message=fault_message,
                                                point_uuid=point.uuid)

    point_store.save_to_db()
