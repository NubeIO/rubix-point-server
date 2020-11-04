from src.models.network.model_network import NetworkModel
from src.models.device.model_device import DeviceModel
from src.models.point.model_point import PointModel


class HistoryBinding:

    def connect(self):
        return

    def post_points_all(self, point_data):
        raise Exception("History Binding post_points_all not implemented")
        return

    def post_points_single(self, point_data):
        raise Exception("History Binding post_points_all not implemented")
        return