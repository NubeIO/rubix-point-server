from flask_restful import marshal_with
from rubix_http.resource import RubixResource

from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.resources.rest_schema.schema_point_store_history import point_store_history_fields


class PointStoryHistoryResource(RubixResource):
    @classmethod
    @marshal_with(point_store_history_fields)
    def get(cls):
        return PointStoreHistoryModel.find_all()


class PointStoreHistoryResourceByPointUUID(RubixResource):
    @classmethod
    @marshal_with(point_store_history_fields)
    def get(cls, point_uuid):
        return PointStoreHistoryModel.find_by_point_uuid(point_uuid)
