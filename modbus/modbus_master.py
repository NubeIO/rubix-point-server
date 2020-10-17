

from pymodbus.client.sync import ModbusTcpClient as TcpClient
from pymodbus.client.sync import ModbusSerialClient as SerialClient
import time, pendulum
import numpy as np


import logging

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class TCP_Client:
    """ Modbus TCP"""

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.client = TcpClient(host=self.host, port=self.port)
        self.connection = self.client.connect()
        if self.connection == False:
            print('Brak Polaczenia z adresem {}:{}'.format(self.host, self.port))


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
        '''
        Auxiliary function
        :return:holding reg
        '''
        self.reg_type = 'holding'
        read = self.client.read_holding_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(read) == False:  # checking for errors
            return read.registers[0:]

    def _read_input(self):
        '''
        Auxiliary function
        :return:
        '''
        self.reg_type = 'input'
        read = self.client.read_input_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(read) == False:  # checking for errors
            return read.registers[0:]

    def _write_single(self):
        '''
        Auxiliary function
        :return:
        '''
        self.reg_type = 'holding'
        read = self.client.write_register(self.reg_add, self.new_val, unit=self.unit)
        if self._assercion(read) == False:  # checking for errors
            return print('Saved value')

    def _read_multiple_colis(self):
        """
        Auxiliary function
        :return:
        """
        self.reg_type = 'coil'
        read = self.client.read_coils(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(read) == False:  # checking for errors
            return read.bits[0:self.reg_lenght]

    def _read_multipe_discrete_inputs(self):
        '''
        Auxiliary function
        :return:
        '''
        self.reg_type = 'disc_input'
        read = self.client.read_discrete_inputs(self.reg_start, self.reg_lenght, unit=self.unit)
        assertion_check = self._assercion(read)
        if assertion_check == False:  # checking for errors
            return read.bits[0:self.reg_lenght]
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # metody pomocnicze
    def _assercion(self, operation):
        '''

        :param operation: Client method. Checks whether data has been downloaded
        :return: Status False to OK or True.
        '''
        # test that we are not an error
        if not operation.isError():
            pass
        else:
            # print("Bład polaczenia z adresem ", self.unit, 'Typ: ', self.reg_type, "Wyjątek: ", operation)
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

    def _choise_data_type(self, data):
        """
        It checks if you need to swap registers and encode to the appropriate format.
        :param data: Log List Downloaded
        :return: List in the data format you need. int, int32, float.
        """
        if self.data_type != 'int':
            if self.transp != False:  # table transposition [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            if self.data_type == 'float':
                # data_arr = np.array([data], dtype=BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big,
                #                                                                      wordorder=Endian.Big).decode_32bit_float())
                data: float = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_32bit_float()
            if self.data_type == 'int32':
                data_arr = np.array([data], dtype=np.int32)
                data_as_int32 = data_arr.view(dtype=np.int32).tolist()[0]  # to list  changes to a list and skips [[]]
                data = data_as_int32
        return data

    def _data_to_dict(self, data):
        """
        Pushes numbered records into the dictionary
        :param data: List with downloaded registers
        :return: Dictionary.
        """
        if self.data_type == 'int' or self.data_type == 'bool':
            dic_val = {str(nr + self.reg_start): v for nr, v in enumerate(data)}
        else:
            dic_val = {str(nr + self.reg_start): v for nr, v in enumerate(data[::2])}  # 0,2,4,6
        return_dict = {'Device': self.unit, 'Reg_type': self.reg_type,
                       'Data_type': self.data_type, 'Time': self.d_now,
                       'Data': dic_val}
        return return_dict

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
    # metody uruchomieniowe
    def read_bool(self, unit, reg_start, reg_lenght, reg_type='coil'):
        '''
        Reading binary registers.
        :param unit: Adres urzadzenia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru.
        :return: Slownik
        '''
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = 'bool'
        self.d_now = self.date_now()

        self.client.connect()  #  IT MAYBE NECESSARY TO CLOSE SESSIONS AT EVERY MEASUREMENT
        if self.reg_type == 'coil':
            measure = self._read_multiple_colis()
        elif self.reg_type == 'disc_input':
            measure = self._read_multipe_discrete_inputs()
        else:
            print("Zly typ rejstru")
        self.client.close()
        if measure != False:
            data_ok = self._data_check(measure)
            if data_ok:
                dicData = self._data_to_dict(measure)  # zamiana na slownik i wydruk
                return dicData

    def write_register(self, unit, reg_add, new_val):
        '''
        Zapis jednego rejestru
        :param unit: Adres urzadzenia.
        :param reg_add: Adres rejetru do zapisu.
        :param new_val: Nowa wartosc rejestru
        :return: list(unit,reg_add,new_val)
        '''
        self.reg_add = reg_add
        self.new_val = new_val
        self.unit = unit
        self.d_now = self.date_now()

        self.client.connect()  # # IT MAYBE NECESSARY TO CLOSE SESSIONS AT EVERY MEASUREMENT
        self._write_single()
        self.client.close()
        return self.unit, self.reg_add, self.new_val

    def read_register(self, unit, reg_start, reg_lenght, reg_type, data_type, transp=False):
        '''

        :param unit: Adres urzadznia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru. ('holding','input','coil','disc_input')
        :param data_type: Typ danych ('int','int32','float')
        :param transp: odwrócenie rejestrow.
        :return: Slownik
        '''
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
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
                d_type = self._choise_data_type(data)  # read result as a list depending on the translation
                # dicData = self._data_to_dict(d_type)  # conversion to a dictionary and printout
                return d_type


# ===================================================================================================================
#
# if __name__ == '__main__':
#
#     staski = TCP_Client('37.26.192.248', 502)
#     print("host:", staski.client.host)
#     print("time out:", staski.client.timeout)
#
#     conn = Master(staski.client)
#     try:
#         reg = conn.read_register(1, 101, 10, reg_type='holding', data_type='int')
#         print(reg)
#     except Exception as e:
#         print(e)
#
#     staski = TCP_Client('37.26.192.248', 502)
#     conn = Master(staski.client)
#     try:
#         coil = conn.read_bool(1, 0, 250, reg_type='coil')
#         input_reg = conn.read_bool(1, 1000, 250, reg_type='coil')
#         print(coil)
#         print(input_reg)
#     except Exception as e:
#         print(e)
#         pass
#
#     try:
#         for k, v in coil['Data'].items():
#             if v == True:
#                 print(k, v)
#     except Exception:
#         pass
#
#     sma = TCP_Client('192.168.0.240', 502)
#     sma_conn = Master(sma.client)
#     try:
#         reg_for_check = [30201, 30233, 30531, 30775, 30795, 30803, 30805, 30813, 30837, 30839, 30769, 30771, 30773,
#                          30957, 30959, 30961, 30537, 30953, 40212, 40915]
#         for i in reg_for_check:
#             reg_sma = sma_conn.read_register(3, i, 2, reg_type='holding', data_type='int32', transp=True)
#             print(reg_sma)
#     except Exception as e:
#         print(e)
#     #
    # cofowent = TCP_Client('192.168.0.30', 502)
    # cofowent_conn = Master(cofowent.client)
    # reg_cofowent = cofowent_conn.read_register(5, 0, 10, reg_type='holding', data_type='int')
    # print(reg_cofowent)
