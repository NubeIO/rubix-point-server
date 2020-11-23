import numbers

from src import TcpRegistry
from src.interfaces.point import HistoryType
from src.source_drivers.modbus.interfaces.network.network import ModbusType
from src.source_drivers.modbus.interfaces.point.points import ModbusPointType
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.models.point.model_point_store import PointStoreModel
from src.source_drivers.modbus.services.modbus_functions.debug import modbus_debug_poll
from src.source_drivers.modbus.services.modbus_functions.polling.poll_funcs import read_input_registers_handle, \
    read_holding_registers_handle, \
    write_coil_handle, \
    read_coils_handle, write_registers_handle
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.services.event_service_base import EventServiceBase, EventTypes, Event
from src.event_dispatcher import EventDispatcher


def poll_point(service: EventServiceBase, network: ModbusNetworkModel, device: ModbusDeviceModel,
               point: ModbusPointModel, transport: ModbusType) -> None:
    """
    Main modbus polling loop
    :param service: EventServiceBase object that's calling this (for point COV events)
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

    mod_device_address = device.address
    reg = point.reg
    mod_point_uuid = point.uuid
    mod_point_reg_length = point.reg_length
    mod_point_type = point.type
    mod_point_data_type = point.data_type
    mod_point_data_endian = point.data_endian

    write_value = point.write_value
    read_coils = ModbusPointType.READ_COILS
    write_coil = ModbusPointType.WRITE_COIL
    read_holding_registers = ModbusPointType.READ_HOLDING_REGISTERS
    read_input_registers = ModbusPointType.READ_INPUT_REGISTERS
    read_input_discrete = ModbusPointType.READ_DISCRETE_INPUTS
    write_registers = ModbusPointType.WRITE_REGISTERS
    """
    DEBUG
    """
    if modbus_debug_poll:
        print("@@@ START MODBUS POLL !!!", {"device": mod_device_address, 'reg': reg})
        print("MODBUS DEBUG:", {'network': network,
                                'device': device,
                                'point':mod_point_uuid,
                                'transport': transport,
                                'mod_device_address': mod_device_address,
                                'reg': reg,
                                'mod_point_reg_length': mod_point_reg_length,
                                'mod_point_type': mod_point_type,
                                'mod_point_data_type': mod_point_data_type,
                                'mod_point_data_endian': mod_point_data_endian,
                                'write_value': write_value
                                })

    fault = False
    fault_message = ""
    point_store_new = None
    try:
        val = None
        array = ""
        """
        read_coils
        """
        if mod_point_type == read_coils:
            val, array = read_coils_handle(connection,
                                           reg,
                                           mod_point_reg_length,
                                           mod_device_address,
                                           mod_point_type)

        """
        read_input_discrete
        """
        if mod_point_type == read_input_discrete:
            val, array = read_coils_handle(connection,
                                           reg,
                                           mod_point_reg_length,
                                           mod_device_address,
                                           mod_point_type)
        """
        write_coils
        """
        if mod_point_type == write_coil:
            val, array = write_coil_handle(connection, reg,
                                           mod_point_reg_length,
                                           mod_device_address,
                                           write_value,
                                           mod_point_type)
        """
        read_input_registers
        """
        if mod_point_type == read_input_registers:
            val, array = read_input_registers_handle(connection,
                                                     reg,
                                                     mod_point_reg_length,
                                                     mod_device_address,
                                                     mod_point_data_type,
                                                     mod_point_data_endian,
                                                     mod_point_type)
        """
        read_holding_registers
        """
        if mod_point_type == read_holding_registers:
            val, array = read_holding_registers_handle(connection,
                                                       reg,
                                                       mod_point_reg_length,
                                                       mod_device_address,
                                                       mod_point_data_type,
                                                       mod_point_data_endian,
                                                       mod_point_type)
        """
        write_registers write_registers
        """
        if mod_point_type == write_registers:
            val, array = write_registers_handle(connection,
                                                reg,
                                                mod_point_reg_length,
                                                mod_device_address,
                                                mod_point_data_type,
                                                mod_point_data_endian,
                                                write_value,
                                                mod_point_type)

        """
        Save modbus data in database
        """
        if modbus_debug_poll:
            print("MODBUS DEBUG: READ/WRITE WAS DONE", 'TRANSPORT TYPE & VAL', {"transport": transport, "val": val})
        if isinstance(val, numbers.Number):
            point_store_new = PointStoreModel(value=val, value_array=str(array), point_uuid=point.uuid)
        else:
            fault = True
            fault_message = "Got non numeric value"
    except Exception as e:
        if modbus_debug_poll:
            print(f'MODBUS ERROR: in poll main function {str(e)}')
        fault = True
        fault_message = str(e)
    if not point_store_new:
        point_store_new = PointStoreModel(fault=fault, fault_message=fault_message, point_uuid=point.uuid)
    if modbus_debug_poll:
        print("!!! END MODBUS POLL @@@")

    is_updated = point_store_new.update()
    if is_updated:
        EventDispatcher.dispatch_from_source(service, Event(EventTypes.POINT_COV, {
            'point': point,
            'point_store': point_store_new,
            'device': device,
            'network': network,
            'source_driver': service.service_name
        }))
        # TODO: move this to history service local as the dispatch event will handle it
        if point.history_type == HistoryType.COV and network.history_enable and \
                device.history_enable and point.history_enable:
            from src import HistoryLocal
            HistoryLocal.add_point_history_on_cov(point.uuid)
