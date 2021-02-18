from typing import List

from src.models.point.model_point_store import PointStoreModel
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase


# TODO: move all to base point_store resource
# TODO: use @marshal_with
class ModbusPointPluralPointStore(ModbusPointBase):
    @classmethod
    def get(cls):
        points: List[ModbusPointModel] = ModbusPointModel.find_all()
        serialized_output = {}
        for point in points:
            if point.device_uuid not in serialized_output:
                serialized_output[point.device_uuid] = []
            serialized_output[point.device_uuid].append(get_point_store(point, point.point_store))
        return serialized_output


class ModbusPointStore(ModbusPointBase):
    @classmethod
    def get(cls, uuid):
        point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(uuid)
        if point_store is None:
            return {}
        else:
            point: ModbusPointModel = ModbusPointModel.find_by_uuid(uuid)
            return get_point_store(point, point_store)


class ModbusDevicePointPluralPointStore(ModbusPointBase):
    @classmethod
    def get(cls, device_uuid):
        points: List[ModbusPointModel] = ModbusPointModel.filter_by_device_uuid(device_uuid)
        serialized_output = []
        for point in points:
            serialized_output.append(get_point_store(point, point.point_store))
        return serialized_output


def get_point_store(point: ModbusPointModel, point_store: PointStoreModel) -> dict:
    return {'uuid': point.uuid, 'name': point.name, 'register': point.register,
            'fault': point_store.fault, 'value': point_store.value}
