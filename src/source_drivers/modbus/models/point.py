from src import db

from src.models.point.model_point_mixin import PointMixinModel
from src.source_drivers.modbus.interfaces.point.points import ModbusFunctionCode, ModbusDataType, ModbusDataEndian


class ModbusPointModel(PointMixinModel):
    __tablename__ = 'modbus_points'

    register = db.Column(db.Integer(), nullable=False)
    register_length = db.Column(db.Integer(), nullable=False)
    function_code = db.Column(db.Enum(ModbusFunctionCode), nullable=False)
    data_type = db.Column(db.Enum(ModbusDataType), nullable=False)
    data_endian = db.Column(db.Enum(ModbusDataEndian), nullable=False, default=ModbusDataEndian.BEB_LEW)
    data_round = db.Column(db.Integer(), nullable=False, default=2)  # TODO: not used
    data_offset = db.Column(db.String(80), nullable=False, default=0)  # TODO: not used
    timeout = db.Column(db.Float(), nullable=False, default=1)  # TODO: not used
    timeout_global = db.Column(db.Boolean(), nullable=False, default=True)  # TODO: not used

    @classmethod
    def get_polymorphic_identity(cls):
        return "Modbus"

    @staticmethod
    def check_can_add(data: dict) -> bool:
        super().check_can_add()
        # register = data.get('register')
        # device_uuid = data.get('device_uuid')
        # function_code = data.get('function_code')
        # db.session.query(db.func.count()).select_from(ModbusPointModel) \
        #     .filter_by(register=register, device_uuid=device_uuid, function_code=function_code)
