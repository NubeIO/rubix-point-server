import logging
import pendulum
import time


from pymodbus.client.sync import ModbusSerialClient as SerialClient
from pymodbus.client.sync import ModbusTcpClient as TcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


class TCP_Client:
    """ Modbus TCP"""

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.client = TcpClient(host=self.host, port=self.port)
        self.connection = self.client.connect()
        if self.connection == False:
            print('There is no connection with the address{}:{}'.format(self.host, self.port))


class RTU_Client:
    """ Modbus RTU"""

    def __init__(self, method, rs_port, speed, stopbits, parity, bytesize, timeout):
        self.method = method
        self.rs_port = rs_port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

        try:
            self.client = SerialClient(method=self.method, port=self.rs_port, baudrate=self.speed,
                                       stopbits=self.stopbits,
                                       parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)
            self.connection = self.client.connect()
            if self.connection == False:
                print('No connection')
                exit(1)
        except Exception as e:
            print(e)
            exit(1)


# ====================================================================================================================

class Master:

    def __init__(self, client):
        self.client = client

    def _read_holding(self):
        """
        Auxiliary function
        :return:holding reg
        """
        self.reg_type = 'holding'
        read = self.client.read_holding_registers(self.reg_start, self.reg_length, unit=self.unit)
        if self._assertion(read) == False:  # checking for errors
            return read.registers[0:]

    def _read_input(self):
        """
        Auxiliary function
        :return:
        """
        self.reg_type = 'input'
        read = self.client.read_input_registers(self.reg_start, self.reg_length, unit=self.unit)
        if self._assertion(read) == False:  # checking for errors
            return read.registers[0:]

    def _write_single(self):
        """
        Auxiliary function
        :return:
        """
        self.reg_type = 'holding'
        read = self.client.write_register(self.reg_add, self.new_val, unit=self.unit)
        if self._assertion(read) == False:  # checking for errors
            return print('Saved value')

    def _read_multiple_colis(self):
        """
        Auxiliary function
        :return:
        """
        self.reg_type = 'coil'
        read = self.client.read_coils(self.reg_start, self.reg_length, unit=self.unit)
        if self._assertion(read) == False:  # checking for errors
            return read.bits[0:self.reg_length]

    def _read_multipe_discrete_inputs(self):
        '''
        Auxiliary function
        :return:
        '''
        self.reg_type = 'disc_input'
        read = self.client.read_discrete_inputs(self.reg_start, self.reg_length, unit=self.unit)
        assertion_check = self._assertion(read)
        if assertion_check == False:  # checking for errors
            return read.bits[0:self.reg_length]
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def _assertion(self, operation):
        """
        :param operation: Client method. Checks whether data has been downloaded
        :return: Status False to OK or True.
        """
        # test that we are not an error
        if not operation.isError():
            pass
        else:
            print("connects to port: {}; Type Register: {}; Exception: {}".format(self.client.port,
                                                                                  self.reg_type,
                                                                                  operation, ))
        return operation.isError()

    def _data_check(self, data):
        """
        Checks whether the object is iterable.
        :param data: Log List Downloaded
        :return: True to OK ,False has issue.
        """
        try:
            iter(data)  # Checks whether the object is iterable
            return True
        except TypeError as e:
            print('No data read out', e)
            return False

    def _select_data_type(self, data):
        """
        It checks if you need to swap registers and encode to the appropriate format.
        :param data: Log List Downloaded
        :return: List in the data format you need. int, int32, float.
        """
        if self.data_type != 'int':
            if self.transp != False:  # table transposition [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            if self.data_type == 'float':
                data: float = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big,
                                                                 wordorder=Endian.Little).decode_32bit_float()
            if self.data_type == 'int32':
                data = data

        return data

    def date_now(self):
        """
        Get time.
        :return: list(timestamp,string)
        """
        _now = pendulum.now()
        self.timestamp = _now.timestamp()
        self.time_string = _now.to_datetime_string()
        return self.timestamp, self.time_string

    # ------------------------------------------------------------------------------------------------------------------
    def read_bool(self, unit, reg_start, reg_length, reg_type='coil'):
        """
        Reading binary registers.
        :param unit:  address
        :param reg_start:
        :param reg_length:
        :param reg_type:
        :return:
        """
        self.unit = unit
        self.reg_start = reg_start
        self.reg_length = reg_length
        self.reg_type = reg_type
        self.data_type = 'bool'
        self.d_now = self.date_now()

        self.client.connect()  # IT MAYBE NECESSARY TO CLOSE SESSIONS AT EVERY MEASUREMENT
        if self.reg_type == 'coil':
            data = self._read_multiple_colis()
        elif self.reg_type == 'disc_input':
            data = self._read_multipe_discrete_inputs()
        else:
            print("point type dosnt exist")
        self.client.close()
        if data != False:
            data_ok = self._data_check(data)
            if data_ok:
                # data = self._data_to_dict(data)
                return data

    def write_register(self, unit, reg_add, new_val):
        """
        :param unit: address
        :param reg_add:
        :param new_val:
        :return: list(unit,reg_add,new_val)
        """
        self.reg_add = reg_add
        self.new_val = new_val
        self.unit = unit
        self.d_now = self.date_now()

        self.client.connect()  # # IT MAYBE NECESSARY TO CLOSE SESSIONS AT EVERY MEASUREMENT
        self._write_single()
        self.client.close()
        return self.unit, self.reg_add, self.new_val

    def read_register(self, unit, reg_start, reg_length, reg_type, data_type, transp=False):
        """
        :param unit: address
        :param reg_start:
        :param reg_length:
        :param reg_type:  ('holding','input','coil','disc_input')
        :param data_type: Data type ('int','int32','float')
        :param transp: tcp or RTU
        :return:
        """
        self.unit = unit
        self.reg_start = reg_start
        self.reg_length = reg_length
        self.reg_type = reg_type
        self.data_type = data_type
        self.transp = transp
        self.d_now = self.date_now()

        self.client.connect()  # IT MAYBE NECESSARY TO CLOSE SESSIONS AT EVERY MEASUREMENT
        time.sleep(0.5)
        if self.reg_type == 'holding':
            data = self._read_holding()
        elif self.reg_type == "input":
            data = self._read_input()
        self.client.close()
        if data != False:
            data_ok = self._data_check(data)
            if data_ok:
                d_type = self._select_data_type(data)  # read result as a list depending on the translation
                return d_type
