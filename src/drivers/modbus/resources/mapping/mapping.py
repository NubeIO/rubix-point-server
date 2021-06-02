import shortuuid
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.drivers.modbus.enums.mapping.mapping import MappingState, MapType
from src.drivers.modbus.models.mapping import MPGBPMapping
from src.drivers.modbus.resources.rest_schema.schema_modbus_mapping import mapping_mp_gbp_attributes, \
    mapping_mp_gbp_all_fields, mapping_mp_gbp_uuid_attributes, mapping_mp_gbp_name_attributes, \
    mapping_mp_gbp_patch_attributes
from src.models.point.model_point_store import PointStoreModel


def sync_point_value(mapping: MPGBPMapping):
    if mapping.mapping_state in (MappingState.MAPPED.name, MappingState.MAPPED):
        point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.point_uuid)
        point_store.sync_point_value_with_mapping_mp_to_gbp(mapping.type, mapping.mapped_point_uuid)
    return mapping


class MPGBPMappingResourceList(RubixResource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def get(cls):
        return MPGBPMapping.find_all()


class MPGBPMappingResourceListByUUID(RubixResource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        for attr in mapping_mp_gbp_uuid_attributes:
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


class MPGBPMappingResourceListByName(RubixResource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        for attr in mapping_mp_gbp_name_attributes:
            parser.add_argument(attr,
                                type=mapping_mp_gbp_attributes[attr].get('type'),
                                required=mapping_mp_gbp_attributes[attr].get('required', False),
                                default=None)
        data = parser.parse_args()
        data.uuid = str(shortuuid.uuid())
        mapping: MPGBPMapping = MPGBPMapping(**data)
        mapping.save_to_db()
        sync_point_value(mapping)
        return mapping


class MPGBMappingResourceUpdateMappingState(RubixResource):
    @classmethod
    def get(cls):
        mappings = MPGBPMapping.find_all()
        for mapping in mappings:
            try:
                mapping.mapping_state = MappingState.MAPPED
                mapping.check_self()
            except ValueError:
                mapping.mapping_state = MappingState.BROKEN
            mapping.commit()
            sync_point_value(mapping)
        return {"message": "Mapping state has been updated successfully"}


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
    for attr in mapping_mp_gbp_patch_attributes:
        parser.add_argument(attr,
                            type=mapping_mp_gbp_attributes[attr].get('type'),
                            required=mapping_mp_gbp_attributes[attr].get('required', False),
                            default=None)

    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def patch(cls, uuid):
        data = MPGBPMappingResourceByUUID.parser.parse_args()
        mapping: MPGBPMapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        mapping.update(**data)
        sync_point_value(mapping)
        return mapping

    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_uuid(uuid)


class MPGBPMappingResourceByModbusPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_point_uuid(uuid)


class MPGBPMappingResourceByGenericPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_mapped_point_uuid_type(uuid, MapType.GENERIC)


class MPGBPMappingResourceByBACnetPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> MPGBPMapping:
        return MPGBPMapping.find_by_mapped_point_uuid_type(uuid, MapType.BACNET)
