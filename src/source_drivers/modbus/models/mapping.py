from mrb.mapper import api_to_topic_mapper
from mrb.message import Response, HttpMethod
from sqlalchemy.orm import validates

from src import db
from src.models.model_base import ModelBase
from src.source_drivers.generic.models.point import GenericPointModel


class MPGBPMapping(ModelBase):
    """
    modbus_point <> generic_point | bacnet_point
    """
    __tablename__ = 'mappings_mp_gbp'

    uuid = db.Column(db.String, primary_key=True)
    modbus_point_uuid = db.Column(db.String, db.ForeignKey('modbus_points.uuid'), nullable=False)
    generic_point_uuid = db.Column(db.String(80), nullable=True, unique=True)
    bacnet_point_uuid = db.Column(db.String(80), nullable=True, unique=True)
    modbus_point_name = db.Column(db.String(80), nullable=False)
    generic_point_name = db.Column(db.String(80), nullable=True)
    bacnet_point_name = db.Column(db.String(80), nullable=True)

    @validates('generic_point_uuid')
    def validate_generic_point_uuid(self, _, value):
        if value:
            generic_point: GenericPointModel = GenericPointModel.find_by_uuid(value)
            if not generic_point:
                raise ValueError(f"Does not exist generic_point_uuid {value}")
        return value

    @validates('bacnet_point_uuid')
    def validate_bacnet_point_uuid(self, _, value):
        if value:
            response: Response = api_to_topic_mapper(api=f'/api/bacnet/points/uuid/{value}',
                                                     destination_identifier='bacnet', http_method=HttpMethod.GET)
            if response.error:
                raise ValueError(response.error_message)
        return value

    @validates('bacnet_point_name')
    def validate_bacnet_point_name(self, _, value):
        self.validate(value)
        return value

    def validate(self, bacnet_point_name: str):
        if not ((self.generic_point_uuid and not self.bacnet_point_uuid) or (
                not self.generic_point_uuid and self.bacnet_point_uuid)):
            raise ValueError("either generic_point_uuid or bacnet_point_uuid should be mapped")
        if self.generic_point_uuid:
            if not self.generic_point_name:
                raise ValueError("generic_point_name should not be null or blank")
            if bacnet_point_name:
                raise ValueError("bacnet_point_name should be null when generic_point_uuid is not null")
        if self.bacnet_point_uuid:
            if not bacnet_point_name:
                raise ValueError("bacnet_point_name should not be null or blank")
            if self.generic_point_name:
                raise ValueError("generic_point_name should be null when bacnet_point_uuid is not null")
        if not self.modbus_point_name:
            raise ValueError("modbus_point_name should not be null or blank")

    @classmethod
    def find_by_modbus_point_uuid(cls, modbus_point_uuid):
        return cls.query.filter_by(modbus_point_uuid=modbus_point_uuid).first()

    @classmethod
    def find_by_generic_point_uuid(cls, generic_point_uuid):
        return cls.query.filter_by(generic_point_uuid=generic_point_uuid).first()

    @classmethod
    def find_by_bacnet_point_uuid(cls, bacnet_point_uuid):
        return cls.query.filter_by(bacnet_point_uuid=bacnet_point_uuid).first()
