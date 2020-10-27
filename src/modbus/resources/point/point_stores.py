from src.modbus.models.point import ModbusPointModel
from src.modbus.models.point_store import ModbusPointStoreModel
from src.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils


class ModbusPointStore(ModbusPointBase):
    def get(self, uuid):
        point = ModbusPointStoreModel.query.filter(ModbusPointStoreModel.point_uuid == uuid).first()
        return ModelUtils.row2dict(point)


class ModbusPointPluralPointStore(ModbusPointBase):
    def get(self):
        points = ModbusPointModel.query.all()
        serialized_output = {}
        for row in points:
            if row.device_uuid not in serialized_output:
                serialized_output[row.device_uuid] = []
            serialized_output[row.device_uuid].append({'uuid': row.uuid, 'name': row.name, 'reg': row.reg,
                                                       'fault': row.value.fault, 'value': row.value.value})
        return serialized_output


class ModbusDevicePointPluralPointStore(ModbusPointBase):
    def get(self, device_uuid):
        points = ModbusPointModel.query.filter(ModbusPointModel.device_uuid == device_uuid)
        serialized_output = []
        for row in points:
            serialized_output.append({'uuid': row.uuid, 'name': row.name, 'reg': row.reg, 'fault': row.value.fault,
                                      'value': row.value.value})
        return serialized_output
