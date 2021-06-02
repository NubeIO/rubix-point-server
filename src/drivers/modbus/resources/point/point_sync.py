from rubix_http.resource import RubixResource

from src.background import Background
from src.models.point.model_point_store import PointStoreModel


class MPToBPSync(RubixResource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values_mp_to_gbp_process(gp=False)


class MPSync(RubixResource):

    @classmethod
    def get(cls):
        Background.sync_on_start()
