import logging
import numbers
from typing import List

from pymodbus.client.sync import BaseModbusClient
from pymodbus.exceptions import ModbusIOException

from src.drivers.modbus.enums.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian
from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.models.network import ModbusNetworkModel
from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.services.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue, write_analogue_aggregate
from src.drivers.modbus.services.polling.function_utils import _mod_point_data_endian, convert_to_data_type, \
    pack_point_write_registers
from src.models.point.model_point_store import PointStoreModel
from src.models.point.priority_array import PriorityArrayModel
from src.services.event_service_base import EventServiceBase

logger = logging.getLogger(__name__)


def poll_point_aggregate(service: EventServiceBase, client: BaseModbusClient, network: ModbusNetworkModel,
                         device: ModbusDeviceModel, point_slice) -> None:
    device_address: int = device.address
    zero_based: bool = device.zero_based
    point_register: int = point_slice[0].register
    point_register_length = 0
    write_values = []
    for point in point_slice:
        point_register_length += point.register_length
        write_values.append(point.write_value)
    point_fc: ModbusFunctionCode = point_slice[0].function_code
    if point_fc is ModbusFunctionCode.WRITE_COIL:
        point_fc = ModbusFunctionCode.WRITE_COILS
    elif point_fc is ModbusFunctionCode.WRITE_REGISTER:
        point_fc = ModbusFunctionCode.WRITE_REGISTERS
    if point_fc is ModbusFunctionCode.WRITE_REGISTERS:
        write_values = pack_point_write_registers(point_slice)
    point_data_endian: ModbusDataEndian = point_slice[0].data_endian

    array = None
    fault = False
    error = None
    try:
        val, array = __poll_point(client, device_address, zero_based, point_register, point_register_length, point_fc,
                                  ModbusDataType.RAW, point_data_endian, write_values)

    except ModbusIOException as e:
        logger.error(str(e))
        fault = True
        fault_message = str(e)
        error = e

    arr_ind = 0
    val = 0
    arr_slice = None if array is None else array[0:1]
    for point in point_slice:
        point_store_new = None
        if not fault:

            if point.data_type is not ModbusDataType.RAW and point.data_type is not ModbusDataType.DIGITAL:
                byteorder, word_order = _mod_point_data_endian(point.data_endian)
                arr_slice = array[arr_ind:arr_ind+point.register_length]
                val = convert_to_data_type(arr_slice, point.data_type, byteorder,
                                           word_order)
            elif point.data_type is ModbusDataType.DIGITAL:
                arr_slice = array[arr_ind:arr_ind+1]
                val = array[arr_ind]
            else:
                arr_slice = array[arr_ind:point.register_length]
                val = array[arr_ind]

            arr_ind += point.register_length

            if isinstance(val, numbers.Number):
                point_store_new = PointStoreModel(value_original=float(str(val)), value_raw=str(arr_slice),
                                                  point_uuid=point.uuid)
            else:
                fault_message = f"Received not numeric value, type is: {type(val)}"
                fault = True
                logger.error(fault_message)

        if not point_store_new:
            point_store_new = PointStoreModel(fault=fault, fault_message=fault_message, point_uuid=point.uuid)

        try:
            if point.update_point_value(point_store_new):
                point.publish_cov(point_store_new, device, network, service.service_name)
        except BaseException as e:
            logger.error(e)

    if error is not None:
        raise error


def poll_point(service: EventServiceBase, client: BaseModbusClient, network: ModbusNetworkModel,
               device: ModbusDeviceModel, point: ModbusPointModel, update: bool) -> PointStoreModel:
    """
    Main modbus polling loop
    :param service: EventServiceBase object that's calling this (for point COV events)
    :param client: pymodbus network connection
    :param network: modbus network class
    :param device: modbus device class
    :param point: modbus point class
    :param update: update point store or not
    :return: PointStoreModel
    """

    device_address: int = device.address
    zero_based: bool = device.zero_based
    point_register: int = point.register
    point_register_length: int = point.register_length
    point_fc: ModbusFunctionCode = point.function_code
    point_data_type: ModbusDataType = point.data_type
    point_data_endian: ModbusDataEndian = point.data_endian
    write_value: float = PriorityArrayModel.get_highest_priority_value_from_dict(point.priority_array_write) or 0

    fault: bool = False
    fault_message: str = ""
    point_store_new = None
    error = None

    try:
        val, array = __poll_point(client, device_address, zero_based, point_register, point_register_length, point_fc,
                                  point_data_type, point_data_endian, [write_value])

        if isinstance(val, numbers.Number):
            point_store_new = PointStoreModel(value_original=float(str(val)), value_raw=str(array),
                                              point_uuid=point.uuid)
        else:
            fault_message = f"Received not numeric value, type is: {type(val)}"
            fault = True
            logger.error(fault_message)

    except ModbusIOException as e:
        logger.error(str(e))
        fault = True
        fault_message = str(e)
        error = e

    if not point_store_new:
        point_store_new = PointStoreModel(fault=fault, fault_message=fault_message, point_uuid=point.uuid)

    if update:
        try:
            is_updated = point.update_point_value(point_store_new, point.driver)
        except BaseException as e:
            logger.error(e)
            return point_store_new
        if is_updated:
            point.publish_cov(point_store_new, device, network, service.service_name)

    if error is not None:
        raise error

    return point_store_new


def __poll_point(client: BaseModbusClient, device_address: int, zero_based: bool,
                 point_register: int, point_register_length: int, point_fc: ModbusFunctionCode,
                 point_data_type: ModbusDataType, point_data_endian: ModbusDataEndian, write_values: List[float]):
    logger.debug('--------------- START MODBUS POLL POINT ---------------')
    logger.debug({'device_address': device_address,
                  'point_fc': point_fc,
                  'point_register': point_register,
                  'point_register_length': point_register_length,
                  'point_data_type': point_data_type,
                  'point_data_endian': point_data_endian,
                  'write_values': write_values
                  })
    # TODO need to confirm, looks suspicious
    if not zero_based:
        point_register -= 1
        logger.debug(f"Device zero_based True, [point_register - 1 = {point_register}]")

    val = None
    array = ""

    if point_fc in [ModbusFunctionCode.READ_COILS, ModbusFunctionCode.READ_DISCRETE_INPUTS]:
        val, array = read_digital(client,
                                  point_register,
                                  point_register_length,
                                  device_address,
                                  point_fc)

    elif point_fc in [ModbusFunctionCode.READ_HOLDING_REGISTERS, ModbusFunctionCode.READ_INPUT_REGISTERS]:
        val, array = read_analogue(client,
                                   point_register,
                                   point_register_length,
                                   device_address,
                                   point_data_type,
                                   point_data_endian,
                                   point_fc)

    elif point_fc in [ModbusFunctionCode.WRITE_COIL, ModbusFunctionCode.WRITE_COILS]:
        val, array = write_digital(client, point_register,
                                   point_register_length,
                                   device_address,
                                   write_values,
                                   point_fc)
    elif point_fc == ModbusFunctionCode.WRITE_REGISTER or (point_fc == ModbusFunctionCode.WRITE_REGISTERS and
                                                           point_data_type is not ModbusDataType.RAW):
        val, array = write_analogue(client,
                                    point_register,
                                    point_register_length,
                                    device_address,
                                    point_data_type,
                                    point_data_endian,
                                    write_values[0],
                                    point_fc)
    elif point_fc is ModbusFunctionCode.WRITE_REGISTERS and point_data_type is ModbusDataType.RAW:
        val, array = write_analogue_aggregate(client,
                                              point_register,
                                              point_register_length,
                                              device_address,
                                              write_values,
                                              point_fc)

    logger.debug(f'READ/WRITE SUCCESS: val: {val}, array: {array}')
    logger.debug("--------------- END MODBUS POLL POINT ---------------")

    return val, array
