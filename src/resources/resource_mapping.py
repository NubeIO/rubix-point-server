from flask_restful import Resource, abort, marshal_with, reqparse
from sqlalchemy.exc import IntegrityError

from src.models.mapping.model_mapping import GBPointMapping
from src.models.point.model_point import PointModel
from src.resources.rest_schema.schema_mapping import bacnet_point_mapping_fields, bacnet_point_mapping_attributes


class GBPMappingResourceList(Resource):
    @classmethod
    @marshal_with(bacnet_point_mapping_fields)
    def get(cls):
        return GBPointMapping.find_all()

    @classmethod
    @marshal_with(bacnet_point_mapping_fields)
    def put(cls):
        parser = reqparse.RequestParser()
        for attr in bacnet_point_mapping_attributes:
            parser.add_argument(attr,
                                type=bacnet_point_mapping_attributes[attr]['type'],
                                required=bacnet_point_mapping_attributes[attr].get('required', False),
                                help=bacnet_point_mapping_attributes[attr].get('help', None),
                                store_missing=False)
        try:
            data = parser.parse_args()
            mapping = GBPointMapping.find_by_generic_point_uuid(data.get('generic_point_uuid'))
            if mapping:
                mapping.update(**data)
                output: GBPointMapping = GBPointMapping.find_by_generic_point_uuid(data.get('generic_point_uuid'))
            else:
                mapping = GBPointMapping(**data)
                mapping.save_to_db()
                output: GBPointMapping = mapping
            point = PointModel.find_by_uuid(mapping.generic_point_uuid)
            point.sync_from_bacnet()
            return output
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))


class GBPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(bacnet_point_mapping_fields)
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


class GBPMappingResourceByGenericPointUUID(GBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return GBPointMapping.find_by_generic_point_uuid(point_uuid)


class GBPMappingResourceByBACnetPointUUID(GBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return GBPointMapping.find_by_bacnet_point_uuid(point_uuid)
