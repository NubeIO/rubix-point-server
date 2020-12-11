import logging
import numbers

from pymodbus.exceptions import ModbusIOException

from src.interfaces.point import HistoryType
from src.loggers import modbus_poll_debug_log
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase
from src.services.histories.history_local import HistoryLocal
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode
from src.source_drivers.modbus.models.device import ModbusDeviceModel
from src.source_drivers.modbus.models.network import ModbusNetworkModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue
from src.source_drivers.modbus.services import modbus_poll_debug


logger = logging.getLogger(modbus_poll_debug_log)


def poll_point(service: EventServiceBase, connection, network: ModbusNetworkModel, device: ModbusDeviceModel,
               point: ModbusPointModel, update: bool) -> PointStoreModel:
    """
    Main modbus polling loop
    :param service: EventServiceBase object that's calling this (for point COV events)
    :param connection: pymodbus network connection
    :param network: modbus network class
    :param device: modbus device class
    :param point: modbus point class
    :param update: update point store or not
    :return: PointStoreModel
    """

    device_address = device.address
    zero_based = device.zero_based
    point_register = point.register
    point_uuid = point.uuid
    point_register_length = point.register_length
    point_fc = point.function_code
    point_data_type = point.data_type
    point_data_endian = point.data_endian
    write_value = point.write_value

    modbus_poll_debug(logger, '--------------- START MODBUS POLL POINT ---------------')
    modbus_poll_debug(logger, {'network': network,
                               'device_uuid': device.uuid,
                               'device_address': device_address,
                               'point_uuid': point_uuid,
                               'point_fc': point_fc,
                               'point_register': point_register,
                               'point_register_length': point_register_length,
                               'point_data_type': point_data_type,
                               'point_data_endian': point_data_endian,
                               'writable': point.writable,
                               'write_value': write_value
                               })
    if not zero_based:
        point_register -= 1
        modbus_poll_debug(logger, f"device zero_based True. point_register -= 1: {point_register + 1} "
                                  f"-> {point_register}")

    fault = False
    fault_message = ""
    point_store_new = None
    error = None

    try:
        val = None
        array = ""

        if point_fc == ModbusFunctionCode.READ_COILS or \
                point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS:
            val, array = read_digital(connection,
                                      point_register,
                                      point_register_length,
                                      device_address,
                                      point_fc)

        elif point_fc == ModbusFunctionCode.READ_HOLDING_REGISTERS or \
                point_fc == ModbusFunctionCode.READ_INPUT_REGISTERS:
            val, array = read_analogue(connection,
                                       point_register,
                                       point_register_length,
                                       device_address,
                                       point_data_type,
                                       point_data_endian,
                                       point_fc)

        elif point_fc == ModbusFunctionCode.WRITE_COIL or \
                point_fc == ModbusFunctionCode.WRITE_COILS:
            val, array = write_digital(connection, point_register,
                                       point_register_length,
                                       device_address,
                                       write_value,
                                       point_fc)
        elif point_fc == ModbusFunctionCode.WRITE_REGISTER or \
                point_fc == ModbusFunctionCode.WRITE_REGISTERS:
            val, array = write_analogue(connection,
                                        point_register,
                                        point_register_length,
                                        device_address,
                                        point_data_type,
                                        point_data_endian,
                                        write_value,
                                        point_fc)

        modbus_poll_debug(logger, f'READ/WRITE SUCCESS: val: {val}, array: {array}')

        if isinstance(val, numbers.Number):
            point_store_new = PointStoreModel(value_original=val, value_raw=str(array), point_uuid=point.uuid)
        else:
            modbus_poll_debug(logger, f"ERROR: non number received, NOTIFY DEVELOPER. type {type(val)}")
            fault = True
            fault_message = f"ERROR: non number received, NOTIFY DEVELOPER. type {type(val)}"

    except ModbusIOException as e:
        modbus_poll_debug(logger, f'ERROR: {str(e)}')
        fault = True
        fault_message = str(e)
        error = e

    if not point_store_new:
        point_store_new = PointStoreModel(fault=fault, fault_message=fault_message, point_uuid=point.uuid)

    modbus_poll_debug(logger, "--------------- END MODBUS POLL POINT ---------------")

    if update:
        try:
            is_updated = point.update_point_value(point_store_new)
        except BaseException as e:
            logger.error(e)
            return point_store_new
        if is_updated:
            point.publish_cov(point_store_new, device, network, service.service_name)
            # TODO: move this to history service local as the dispatch event will handle it
            if point.history_type == HistoryType.COV and network.history_enable and \
                    device.history_enable and point.history_enable:
                HistoryLocal.add_point_history_on_cov(point.uuid)

    if error is not None:
        raise error

    return point_store_new
