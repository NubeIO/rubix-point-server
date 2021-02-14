import uuid as uuid_

from flask_restful import Resource, marshal_with, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.mapping import MPGBPMapping
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_mapping import mapping_mp_gbp_attributes, \
    mapping_mp_gbp_all_fields


class MPGBPMappingResourceList(Resource):
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
        try:
            data = parser.parse_args()
            data.uuid = str(uuid_.uuid4())
            mapping = MPGBPMapping(**data)
            mapping.save_to_db()
            # TODO: sync
            return mapping
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class MPGBPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(mapping_mp_gbp_all_fields)
    def get(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            abort(404, message=f'Does not exist {uuid}')
        return mapping

    @classmethod
    def delete(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if mapping is None:
            abort(404, message=f'Does not exist {uuid}')
        else:
            mapping.delete_from_db()
        return '', 204


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
        mapping = cls.get_mapping(uuid)
        if not mapping:
            abort(404, message='Does not exist {}'.format(uuid))
        try:
            MPGBPMapping.filter_by_uuid(uuid).update(data)
            MPGBPMapping.commit()
            # TODO: sync
            return cls.get_mapping(uuid)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def get_mapping(cls, uuid):
        return MPGBPMapping.find_by_uuid(uuid)


class MPGBPMappingResourceByModbusPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return MPGBPMapping.find_by_modbus_point_uuid(uuid)


class MPGBPMappingResourceByGenericPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return MPGBPMapping.find_by_generic_point_uuid(uuid)


class MPGBPMappingResourceByBACnetPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return MPGBPMapping.find_by_bacnet_point_uuid(uuid)
