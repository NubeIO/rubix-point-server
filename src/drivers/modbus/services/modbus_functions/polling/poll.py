import logging
import numbers

from pymodbus.client.sync import BaseModbusClient
from pymodbus.exceptions import ModbusIOException

from src.drivers.modbus.enums.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian
from src.drivers.modbus.models.device import ModbusDeviceModel
from src.drivers.modbus.models.network import ModbusNetworkModel
from src.drivers.modbus.models.point import ModbusPointModel
from src.drivers.modbus.services.modbus_functions.polling.functions import read_digital, write_digital, \
    read_analogue, write_analogue
from src.models.point.model_point_store import PointStoreModel
from src.services.event_service_base import EventServiceBase

logger = logging.getLogger(__name__)


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
    point_uuid: str = point.uuid
    point_register_length: int = point.register_length
    point_fc: ModbusFunctionCode = point.function_code
    point_data_type: ModbusDataType = point.data_type
    point_data_endian: ModbusDataEndian = point.data_endian
    write_value: float = point.write_value if point.write_value else 0

    logger.debug('--------------- START MODBUS POLL POINT ---------------')
    logger.debug({'network': network,
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
    # TODO need to confirm, looks suspicious
    if not zero_based:
        point_register -= 1
        logger.debug(f"Device zero_based True, [point_register - 1 = {point_register}]")

    fault: bool = False
    fault_message: str = ""
    point_store_new = None
    error = None

    try:
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
                                       int(write_value),
                                       point_fc)
        elif point_fc in [ModbusFunctionCode.WRITE_REGISTER, ModbusFunctionCode.WRITE_REGISTERS]:
            val, array = write_analogue(client,
                                        point_register,
                                        point_register_length,
                                        device_address,
                                        point_data_type,
                                        point_data_endian,
                                        write_value,
                                        point_fc)

        logger.debug(f'READ/WRITE SUCCESS: val: {val}, array: {array}')

        if isinstance(val, numbers.Number):
            point_store_new = PointStoreModel(value_original=float(str(val)),
                                              value_raw=str(array),
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
    logger.debug("--------------- END MODBUS POLL POINT ---------------")

    if update:
        try:
            is_updated = point.update_point_value(point_store_new)
        except BaseException as e:
            logger.error(e)
            return point_store_new
        if is_updated:
            point.publish_cov(point_store_new, device, network, service.service_name)

    if error is not None:
        raise error

    return point_store_new
