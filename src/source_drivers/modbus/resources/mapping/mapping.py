from flask_restful import Resource, marshal_with, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.source_drivers.modbus.models.mapping import MPGBPMapping
from src.source_drivers.modbus.resources.rest_schema.schema_modbus_mapping import mp_gbp_mapping_fields, \
    mp_gbp_mapping_attributes


class MPGBPMappingResourceList(Resource):
    @classmethod
    @marshal_with(mp_gbp_mapping_fields)
    def get(cls):
        return MPGBPMapping.find_all()

    @classmethod
    @marshal_with(mp_gbp_mapping_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        for attr in mp_gbp_mapping_attributes:
            parser.add_argument(attr,
                                type=mp_gbp_mapping_attributes[attr].get('type'),
                                required=mp_gbp_mapping_attributes[attr].get('required', False),
                                default=None)
        try:
            data = parser.parse_args()
            print('data', data)
            mapping = MPGBPMapping(**data)
            mapping.save_to_db()
            return mapping
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class MPGBPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(mp_gbp_mapping_fields)
    def get(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if not mapping:
            abort(404, message=f'Does not exist {point_uuid}')
        return mapping

    @classmethod
    def delete(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if mapping is None:
            abort(404, message=f'Does not exist {point_uuid}')
        else:
            mapping.delete_from_db()
        return '', 204


class MPGBPMappingResourceByModbusPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return MPGBPMapping.find_by_modbus_point_uuid(point_uuid)


class MPGBPMappingResourceByGenericPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return MPGBPMapping.find_by_generic_point_uuid(point_uuid)


class MPGBPMappingResourceByBACnetPointUUID(MPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return MPGBPMapping.find_by_bacnet_point_uuid(point_uuid)
