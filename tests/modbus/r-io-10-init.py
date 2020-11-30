import argparse
import time
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian


parser = argparse.ArgumentParser(description='Nube iO R-IO-10 initialiser.')
parser.add_argument('port', metavar='PORT', type=str, help='serial port')
parser.add_argument('baud', metavar='BAUD', type=int, help='serial port baudrate')
parser.add_argument('address', metavar='ADDRESS', type=int, help='slave address')
parser.add_argument('--uo-configs', metavar='n', type=int, nargs='+', help='UO config values (int) (i.e. 1 2)')
parser.add_argument('--ui-configs', metavar='n', type=int, nargs='+', help='UI config values (int) (i.e. 3 1)')
parser.add_argument('--uo-writes', metavar='n', type=float, nargs='+', help='UO write values (float),  (i.e. 0.1, 12)')
parser.add_argument('--do-writes', metavar='n', type=int, nargs='+', help='DO write values (int) (i.e. 0 1)')
parser.add_argument('--loop', type=float, nargs='?', help='Poll loop seconds (default: 5)', default=5)

UO_DEFAULTS = [1, 2]
UI_DEFAULTS = [3, 1]

args = parser.parse_args()
port = args.port
baud = args.baud
address = args.address
UO_configs = args.uo_configs or UO_DEFAULTS
UI_configs = args.ui_configs or UI_DEFAULTS
UO_writes = args.uo_writes
DO_writes = args.do_writes
poll_loop = args.loop or 5


UO_config_offset = 5 - 1
UI_config_offset = 7 - 1
UO_CONFIG_NAMES = ['RAW', '0-10VDC', '0-12VDC']
UI_CONFIG_NAMES = ['RAW', '0-10ADC', '10k (resistance)', '10k (type 2 temp)', '20k', '4-20MA', 'Pulse Count']


def init_UO(points):
    for offset in range(len(points)):
        res = connection.write_register(UO_config_offset + offset, points[offset], unit=address)
        if res.isError():
            print(f'    ERROR: failed to set UO{offset + 1}')
        else:
            print(f'    set UO{offset + 1} to {UO_CONFIG_NAMES[points[offset]]}')


def init_UI(points):
    for offset in range(len(points)):
        res = connection.write_register(UI_config_offset + offset, points[offset], unit=address)
        if res.isError():
            print(f'    ERROR: failed to set UI{offset + 1}')
        else:
            print(f'    set UI{offset + 1} to {UI_CONFIG_NAMES[points[offset]]}')


def write_UO(points):
    print('    UO')
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    for offset in range(len(points)):
        builder.add_32bit_float(points[offset])
        res = connection.write_registers((offset * 2), builder.to_registers(), unit=address)
        if res.isError():
            print(f'        ERROR: failed to write UO{offset + 1} value {points[offset]}')
        else:
            print(f'        UO{offset + 1} : {points[offset]}')
        builder.reset()


def write_DO(points):
    print('    DO')
    for offset in range(len(points)):
        res = connection.write_coil(offset, points[offset], unit=address)
        if res.isError():
            print(f'        ERROR: failed to write DO{offset + 1} value {points[offset]}')
        else:
            print(f'        DO{offset + 1} : {points[offset]}')


def read_UI(points):
    print('    UI')
    decoder = BinaryPayloadDecoder(None, byteorder=Endian.Big, wordorder=Endian.Little)
    for offset in range(len(points)):
        res = connection.read_input_registers((offset * 2), 2, unit=address)
        if res.isError():
            print(f'        ERROR: failed to read UI{offset + 1}', )
        else:
            value = decoder.fromRegisters(res.registers, byteorder=Endian.Big, wordorder=Endian.Little)\
                .decode_32bit_float()
            print(f'        UI{offset + 1} : {value}')
        decoder.reset()


if __name__ == '__main__':
    print(f'CONNECTION: {port} {baud}')
    print(f'    Slave address: {address}')
    connection = ModbusSerialClient(method='rtu', port=port, baudrate=baud)
    if not connection.connect() and not connection.is_socket_open():
        print(f'failed to connect to serial port {port}')
        exit(1)

    print('INITIALISING R-IO-10...')
    init_UO(UO_configs)
    init_UI(UI_configs)
    print(f'POLLING ({poll_loop} secs)')
    while True:
        if DO_writes is not None:
            write_DO(DO_writes)
        if UO_writes is not None:
            write_UO(UO_writes)
        read_UI(UI_configs)
        print()
        time.sleep(poll_loop)
