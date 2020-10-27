from src.source_drivers.modbus.models.point import ModbusPointModel
from src.models.point.model_point_store import PointStoreModel
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils

# TODO: move all to base point_store resource


class ModbusPointStore(ModbusPointBase):
    @classmethod
    def get(cls, uuid):
        point = PointStoreModel.query.filter(PointStoreModel.point_uuid == uuid).first()
        if point is None:
            return {}
        else:
            return ModelUtils.row2dict(point)


class ModbusPointPluralPointStore(ModbusPointBase):
    @classmethod
    def get(cls):
        points = ModbusPointModel.query.all()
        serialized_output = {}
        for row in points:
            if row.device_uuid not in serialized_output:
                serialized_output[row.device_uuid] = []
            serialized_output[row.device_uuid].append({'uuid': row.uuid, 'name': row.name, 'reg': row.reg,
                                                       'fault': row.value.fault, 'value': row.value.value})
        return serialized_output


class ModbusDevicePointPluralPointStore(ModbusPointBase):
    @classmethod
    def get(cls, device_uuid):
        points = ModbusPointModel.query.filter(ModbusPointModel.device_uuid == device_uuid)
        serialized_output = []
        for row in points:
            serialized_output.append({'uuid': row.uuid, 'name': row.name, 'reg': row.reg, 'fault': row.value.fault,
                                      'value': row.value.value})
        return serialized_output
