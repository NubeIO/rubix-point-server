from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.drivers.modbus.enums.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian
from src.models.point.model_point_mixin import PointMixinModel
from src.models.point.priority_array import PriorityArrayModel


class ModbusPointModel(PointMixinModel):
    __tablename__ = 'modbus_points'

    register = db.Column(db.Integer(), nullable=False)
    register_length = db.Column(db.Integer(), nullable=False)
    function_code = db.Column(db.Enum(ModbusFunctionCode), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False, default=ModbusDataType.RAW)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False, default=ModbusDataEndian.BEB_LEW)
    modbus_device_uuid_constraint = db.Column(db.String, nullable=False)

    __table_args__ = (
        UniqueConstraint('register', 'function_code', 'modbus_device_uuid_constraint'),
    )

    @classmethod
    def filter_by_device_uuid(cls, device_uuid: str):
        return cls.query.filter_by(device_uuid=device_uuid)

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.MODBUS

    @classmethod
    def create_temporary_from_string(cls, string: str):
        split_string = string.split(':')
        if len(split_string) != 3:
            raise ValueError('Invalid Modbus Point string format ("<FC>:<Register>:<Length>')
        data = {
            'function_code': int(split_string[0]),
            'register': int(split_string[1]),
            'register_length': int(split_string[2]),
        }
        point = cls.create_temporary(**data)
        point.validate_function_code(None, point.function_code)
        point.validate_register(None, point.register)
        point.validate_register_length(None, point.register_length)
        return point

    @validates('function_code')
    def validate_function_code(self, _, value):
        if isinstance(value, ModbusFunctionCode):
            function_code: ModbusFunctionCode = value
        elif isinstance(value, int):
            try:
                function_code: ModbusFunctionCode = ModbusFunctionCode(value)
            except Exception:
                raise ValueError("Invalid function code")
        else:
            if not value or value not in ModbusFunctionCode.__members__:
                raise ValueError("Invalid function code")
            function_code: ModbusFunctionCode = ModbusFunctionCode[value]
        if self.is_writable(function_code):
            if PriorityArrayModel.get_highest_priority_value_from_priority_array(self.priority_array_write) is None:
                raise ValueError(f"priority_array_write shouldn't be null for {function_code}")
        return function_code

    @validates('register')
    def validate_register(self, _, value):
        if value < 0 or value > 65535:
            raise ValueError('Invalid register')
        return value

    @validates('register_length')
    def validate_register_length(self, _, value):
        if value < 0 or value > 65535:
            raise ValueError('Invalid register length')
        return value

    @validates('data_type')
    def validate_data_type(self, _, value):
        if isinstance(value, ModbusDataType):
            return value
        if not value or value not in ModbusDataType.__members__:
            raise ValueError("Invalid data type")
        return ModbusDataType[value]

    @validates('data_endian')
    def validate_data_endian(self, _, value):
        if isinstance(value, ModbusDataEndian):
            return value
        if not value or value not in ModbusDataEndian.__members__:
            raise ValueError("Invalid data endian")
        return ModbusDataEndian[value]

    def check_self(self) -> (bool, any):
        super().check_self()
        self.modbus_device_uuid_constraint = self.device_uuid

        reg_length = self.register_length
        point_fc: ModbusFunctionCode = self.function_code

        if self.is_writable(point_fc):
            self.writable = True
            if reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_COIL:
                self.function_code = ModbusFunctionCode.WRITE_COILS
            elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_COILS:
                self.function_code = ModbusFunctionCode.WRITE_COIL
            elif reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_REGISTER:
                self.function_code = ModbusFunctionCode.WRITE_REGISTERS
            elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_REGISTERS:
                self.function_code = ModbusFunctionCode.WRITE_REGISTER
        else:
            self.writable = False
            self.priority_array_write = None

        data_type = self.data_type
        if not isinstance(data_type, ModbusDataType):
            data_type = ModbusDataType[self.data_type]
        if point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS or point_fc == ModbusFunctionCode.READ_COILS or \
                point_fc == ModbusFunctionCode.WRITE_COIL:
            data_type = ModbusDataType.DIGITAL
            self.data_type = ModbusDataType.DIGITAL
            self.register_length = 1
            self.value_round = 0

        if data_type == ModbusDataType.FLOAT or data_type == ModbusDataType.INT32 or \
                data_type == ModbusDataType.UINT32:
            self.register_length = 2

        return True

    @staticmethod
    def is_writable(value: ModbusFunctionCode) -> bool:
        return value in [ModbusFunctionCode.WRITE_COIL, ModbusFunctionCode.WRITE_COILS,
                         ModbusFunctionCode.WRITE_REGISTER, ModbusFunctionCode.WRITE_REGISTERS]
