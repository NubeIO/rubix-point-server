import uuid as uuid_
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.drivers.modbus.models.mapping import MPGBPMapping
from src.drivers.modbus.resources.rest_schema.schema_modbus_mapping import mapping_mp_gbp_attributes, \
    mapping_mp_gbp_all_fields
from src.models.point.model_point_store import PointStoreModel


def sync_point_value(mapping: MPGBPMapping):
    point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.modbus_point_uuid)
    point_store.sync_point_value_with_mapping_mp_to_gbp(mapping.generic_point_uuid, mapping.bacnet_point_uuid)
    return mapping


class MPGBPMappingResourceList(RubixResource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def get(cls):
        return MPGBPMapping.find_all()

    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        for attr in mapping_mp_gbp_attributes:
            parser.add_argument(attr,
                                type=mapping_mp_gbp_attributes[attr].get('type'),
                                required=mapping_mp_gbp_attributes[attr].get('required', False),
                                default=None)
        data = parser.parse_args()
        data.uuid = str(uuid_.uuid4())
        mapping: MPGBPMapping = MPGBPMapping(**data)
        mapping.save_to_db()
        sync_point_value(mapping)
        return mapping


class MPGBPMappingResourceBase(RubixResource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def get(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        return mapping

    @classmethod
    def delete(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if mapping is None:
            raise NotFoundException(f'Does not exist {uuid}')
        mapping.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        raise NotImplementedError


class MPGBPMappingResourceByUUID(MPGBPMappingResourceBase):
    parser = reqparse.RequestParser()
    for attr in mapping_mp_gbp_attributes:
        parser.add_argument(attr,
                            type=mapping_mp_gbp_attributes[attr].get('type'),
                            default=None)

    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def patch(cls, uuid):
        data = MPGBPMappingResourceByUUID.parser.parse_args()
        mapping: MPGBPMapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        MPGBPMapping.filter_by_uuid(uuid).update(data)
        MPGBPMapping.commit()
        output_mapping: MPGBPMapping = cls.get_mapping(uuid)
        sync_point_value(mapping)
        return output_mapping

    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_uuid(uuid)


class MPGBPMappingResourceByModbusPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_modbus_point_uuid(uuid)


class MPGBPMappingResourceByGenericPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_generic_point_uuid(uuid)


class MPGBPMappingResourceByBACnetPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_bacnet_point_uuid(uuid)
