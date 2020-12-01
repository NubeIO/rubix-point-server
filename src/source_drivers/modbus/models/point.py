from sqlalchemy import UniqueConstraint

from src import db
from src.models.point.model_point_mixin import PointMixinModel
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian, \
    MathOperation


class ModbusPointModel(PointMixinModel):
    __tablename__ = 'modbus_points'

    register = db.Column(db.Integer(), nullable=False)
    register_length = db.Column(db.Integer(), nullable=False)
    function_code = db.Column(db.Enum(ModbusFunctionCode), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False, default=ModbusDataEndian.BEB_LEW)
    data_round = db.Column(db.Integer(), nullable=False, default=2)
    data_offset = db.Column(db.Integer(), nullable=False, default=0)
    timeout = db.Column(db.Float(), nullable=False, default=1)  # TODO: not used
    timeout_global = db.Column(db.Boolean(), nullable=False, default=True)  # TODO: not used
    math_operation = db.Column(db.Enum(MathOperation), nullable=True)
    math_operation_value = db.Column(db.Float(), nullable=False, default=0)
    modbus_device_uuid_constraint = db.Column(db.String, nullable=False)

    __table_args__ = (
        UniqueConstraint('register', 'function_code', 'modbus_device_uuid_constraint'),
    )

    @classmethod
    def get_polymorphic_identity(cls):
        return "Modbus"

    def check_self(self) -> (bool, any):
        super().check_self()
        self.modbus_device_uuid_constraint = self.device_uuid

        reg_length = self.register_length
        point_fc = self.function_code
        if not isinstance(point_fc, ModbusFunctionCode):
            point_fc = ModbusFunctionCode[self.function_code]

        if point_fc == ModbusFunctionCode.WRITE_COIL or point_fc == ModbusFunctionCode.WRITE_REGISTER \
                or point_fc == ModbusFunctionCode.WRITE_COILS or point_fc == ModbusFunctionCode.WRITE_REGISTERS:
            self.writable = True

            if reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_COIL:
                self.function_code = ModbusFunctionCode.WRITE_COILS
            elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_COILS:
                self.function_code = ModbusFunctionCode.WRITE_COIL
            elif reg_length > 1 and point_fc == ModbusFunctionCode.WRITE_REGISTER:
                self.function_code = ModbusFunctionCode.WRITE_REGISTERS
            elif reg_length == 1 and point_fc == ModbusFunctionCode.WRITE_REGISTERS:
                self.function_code = ModbusFunctionCode.WRITE_REGISTER

        elif point_fc == ModbusFunctionCode.READ_COILS or point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS or \
                point_fc == ModbusFunctionCode.READ_HOLDING_REGISTERS or \
                point_fc == ModbusFunctionCode.READ_INPUT_REGISTERS:
            self.writable = False
            self.write_value = None

        data_type = self.data_type
        if not isinstance(data_type, ModbusDataType):
            data_type = ModbusDataType[self.data_type]
        if point_fc == ModbusFunctionCode.READ_DISCRETE_INPUTS or point_fc == ModbusFunctionCode.READ_COILS or \
                point_fc == ModbusFunctionCode.WRITE_COIL or point_fc == ModbusFunctionCode.WRITE_COILS:
            data_type = ModbusDataType.DIGITAL
            self.data_type = ModbusDataType.DIGITAL
            self.data_round = 0

        if data_type == ModbusDataType.FLOAT or data_type == ModbusDataType.INT32 or \
                data_type == ModbusDataType.UINT32:
            assert reg_length % 2 == 0, f'register_length invalid for data_type {data_type}'

        return True
