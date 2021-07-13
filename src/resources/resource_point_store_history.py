from flask_restful import marshal_with
from flask_restful.reqparse import request
from rubix_http.resource import RubixResource

from src.models.point.model_point_store_history import PointStoreHistoryModel
from src.resources.rest_schema.schema_point_store_history import paginated_point_store_history_fields


class PointStoryHistoryResource(RubixResource):
    @classmethod
    @marshal_with(paginated_point_store_history_fields)
    def get(cls):
        page = request.args.get('page', default=None, type=int)
        per_page = request.args.get('per_page', default=None, type=int)
        sort = request.args.get('sort', default=None, type=str)
        return PointStoreHistoryModel.find_by_pagination(page, per_page, sort)


class PointStoreHistoryResourceByPointUUID(RubixResource):
    @classmethod
    @marshal_with(paginated_point_store_history_fields)
    def get(cls, point_uuid):
        page = request.args.get('page', default=None, type=int)
        per_page = request.args.get('per_page', default=None, type=int)
        sort = request.args.get('sort', default=None, type=str)
        return PointStoreHistoryModel.find_by_point_uuid_pagination(point_uuid, page, per_page, sort)
