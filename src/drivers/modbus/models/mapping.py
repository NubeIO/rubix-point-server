import json

from flask import Response
from rubix_http.request import gw_request
from sqlalchemy.orm import validates

from src import db
from src.drivers.modbus.enums.mapping.mapping import MapType, MappingState
from src.models.model_base import ModelBase


class MPGBPMapping(ModelBase):
    """
    modbus_point <> generic_point | bacnet_point
    """
    __tablename__ = 'mappings_mp_gbp'

    uuid = db.Column(db.String, primary_key=True)
    point_uuid = db.Column(db.String, db.ForeignKey('modbus_points.uuid'), nullable=False)
    mapped_point_uuid = db.Column(db.String(80), nullable=True, unique=True)
    point_name = db.Column(db.String(80), nullable=False)
    mapped_point_name = db.Column(db.String(80), nullable=True)
    type = db.Column(db.Enum(MapType), nullable=True)
    mapping_state = db.Column(db.Enum(MappingState), default=MappingState.MAPPED)

    @validates('type')
    def validate_type(self, _, value):
        if not value:
            raise ValueError("type should not be null or blank")
        return value

    def check_self(self) -> (bool, any):
        super().check_self()
        if self.point_uuid:
            self.__set_point_name()
        if self.mapped_point_uuid:
            self.__set_mapped_point_name()
        if not self.point_uuid:
            self.__set_point_uuid()
        if not self.mapped_point_uuid:
            self.__set_mapped_point_uuid()

    def set_uuid_with_name(self):
        self.__set_point_uuid()
        self.__set_mapped_point_uuid()

    def __set_point_name(self):
        from src.drivers.modbus.models.point import ModbusPointModel
        if not self.point_uuid:
            raise ValueError("point_uuid should not be null or blank")
        modbus_point: ModbusPointModel = ModbusPointModel.find_by_uuid(self.point_uuid)
        if not modbus_point:
            raise ValueError(f"Does not exist point_uuid {self.point_uuid}")
        self.point_name = f"{modbus_point.device.network.name}:{modbus_point.device.name}:{modbus_point.name}"

    def __set_mapped_point_name(self):
        from src.drivers.generic.models.point import GenericPointModel
        if not self.mapped_point_uuid:
            raise ValueError("mapped_point_uuid should not be null or blank")
        if self.type in (MapType.GENERIC.name, MapType.GENERIC):
            generic_point: GenericPointModel = GenericPointModel.find_by_uuid(self.mapped_point_uuid)
            if not generic_point:
                raise ValueError(f"Does not exist mapped_point_uuid {self.mapped_point_uuid}")
            self.mapped_point_name = f"{generic_point.device.network.name}:{generic_point.device.name}:" \
                                     f"{generic_point.name}"
        elif self.type in (MapType.BACNET.name, MapType.BACNET):
            response: Response = gw_request(api=f'/bacnet/api/bacnet/points/uuid/{self.mapped_point_uuid}')
            if response.status_code != 200:
                raise ValueError(f"Does not exist mapped_point_uuid {self.mapped_point_uuid}")
            self.mapped_point_name = json.loads(response.data).get('object_name')
        else:
            raise ValueError(f"Invalid type {self.type}.")

    def __set_point_uuid(self):
        from src.drivers.modbus.models.point import ModbusPointModel
        point_names = self.point_name.split(":")
        if len(point_names) != 3:
            raise ValueError("point_name should be colon (:) delimited network_name:device_name:point_name")
        network_name, device_name, point_name = self.point_name.split(":")
        modbus_point: ModbusPointModel = ModbusPointModel.find_by_name(network_name, device_name, point_name)
        if not modbus_point:
            raise ValueError(f"Does not exist point_name {self.point_name}")
        self.point_uuid = modbus_point.uuid

    def __set_mapped_point_uuid(self):
        from src.drivers.generic.models.point import GenericPointModel
        if not self.mapped_point_name:
            raise ValueError("mapped_point_name should not be null or blank")
        if self.type in (MapType.GENERIC.name, MapType.GENERIC):
            mapped_point_names = self.mapped_point_name.split(":")
            if len(mapped_point_names) != 3:
                raise ValueError(
                    "mapped_point_names should be colon (:) delimited network_name:device_name:point_name")
            network_name, device_name, point_name = mapped_point_names
            generic_point: GenericPointModel = GenericPointModel.find_by_name(network_name, device_name, point_name)
            if not generic_point:
                raise ValueError(f"Does not exist mapped_point_name {self.mapped_point_name}")
            self.mapped_point_uuid = generic_point.uuid
        elif self.type in (MapType.BACNET.name, MapType.BACNET):
            response: Response = gw_request(api=f'/bacnet/api/bacnet/points/name/{self.mapped_point_name}')
            if response.status_code != 200:
                raise ValueError(f"Does not exist mapped_point_name {self.mapped_point_name}")
            self.mapped_point_uuid = json.loads(response.data).get('uuid')
        else:
            raise ValueError(f"Invalid type {self.type}")

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def find_by_mapped_point_uuid_type(cls, mapped_point_uuid, map_type):
        return cls.query.filter_by(mapped_point_uuid=mapped_point_uuid, type=map_type).first()
