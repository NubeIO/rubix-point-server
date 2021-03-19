from rubix_http.resource import RubixResource

from src.models.point.model_point_store import PointStoreModel


class MPBPSync(RubixResource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values_mp_to_gbp_process(gp=False)
