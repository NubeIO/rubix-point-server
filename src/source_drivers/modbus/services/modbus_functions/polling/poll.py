import logging
import numbers

from sqlalchemy.orm.exc import ObjectDeletedError

from src.event_dispatcher import EventDispatcher
from src.interfaces.point import HistoryType
from src.loggers import modbus_debug_poll
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase, EventTypes, Event
from src.source_drivers.modbus.interfaces.network.network import ModbusType
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.services.modbus_functions.polling.poll_funcs import read_digital_handle, \
    read_analog_handle, write_coil_handle, write_holding_registers_handle
from src.source_drivers.modbus.services.rtu_registry import RtuRegistry
from src.source_drivers.modbus.services.tcp_registry import TcpRegistry

logger = logging.getLogger(modbus_debug_poll)


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

    try:
        device_address = device.address
        zero_based = device.zero_based
        point_register = point.register
        point_uuid = point.uuid
        point_register_length = point.register_length
        point_fc = point.function_code
        point_data_type = point.data_type
        point_data_endian = point.data_endian
        write_value = point.write_value
    except ObjectDeletedError:
        return

    logger.debug('@@@ START MODBUS POLL !!!')
    logger.debug({'network': network,
                  'transport': transport,
                  'device_uuid': device.uuid,
                  'device_address': device_address,
                  'point_uuid': point_uuid,
                  'point_register': point_register,
                  'point_register_length': point_register_length,
                  'point_fc': point_fc,
                  'point_data_type': point_data_type,
                  'point_data_endian': point_data_endian,
                  'write_value': write_value
                  })
    if not zero_based:
        point_register -= 1
        logger.debug(f"MODBUS DEBUG: device zero_based True. point_register -= 1: {point_register + 1} "
                     f"-> {point_register}")

    fault = False
    fault_message = ""
    point_store_new = None

    try:
        val = None
        array = ""
        """
        read_coils read_discrete_inputs
        """
        if point_fc == ModbusFunctionCode.READ_COILS or point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS:
            val, array = read_digital_handle(connection,
                                             point_register,
                                             point_register_length,
                                             device_address,
                                             point_fc)
        """
        read_holding_registers read_input_registers
        """
        if point_fc == ModbusFunctionCode.READ_HOLDING_REGISTERS or point_fc == ModbusFunctionCode.READ_INPUT_REGISTERS:
            val, array = read_analog_handle(connection,
                                            point_register,
                                            point_register_length,
                                            device_address,
                                            point_data_type,
                                            point_data_endian,
                                            point_fc)
        """
        write_coils
        """
        if point_fc == ModbusFunctionCode.WRITE_COIL or point_fc == ModbusFunctionCode.WRITE_COILS:
            val, array = write_coil_handle(connection, point_register,
                                           point_register_length,
                                           device_address,
                                           write_value,
                                           point_fc)
        """
        write_registers
        """
        if point_fc == ModbusFunctionCode.WRITE_REGISTER or point_fc == ModbusFunctionCode.WRITE_REGISTERS:
            val, array = write_holding_registers_handle(connection,
                                                        point_register,
                                                        point_register_length,
                                                        device_address,
                                                        point_data_type,
                                                        point_data_endian,
                                                        write_value,
                                                        point_fc)

        """
        Save modbus data in database
        """
        logger.debug(f'MODBUS DEBUG: READ/WRITE WAS DONE: {{"transport": {transport}, "val": {val}}}')
        if isinstance(val, numbers.Number):
            point_store_new = PointStoreModel(value=val, value_array=str(array), point_uuid=point.uuid)
        else:
            fault = True
            fault_message = "Got non numeric value"
    except ObjectDeletedError:
        return
    except Exception as e:
        logger.debug(f'MODBUS ERROR: in poll main function {str(e)}')
        fault = True
        fault_message = str(e)
    if not point_store_new:
        point_store_new = PointStoreModel(fault=fault, fault_message=fault_message, point_uuid=point.uuid)
    logger.debug("!!! END MODBUS POLL @@@")

    try:
        is_updated = point_store_new.update()
    except Exception:
        return
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
