from src.services.histories.history_binding import HistoryBinding


class Influx(HistoryBinding):

    _push_period_minutes = 1

    _instance = None
    _client = None

    host = None
    port = None
    database_name = None
    username = None
    password = None

    def connect(self):
        # TODO: check client already connected
        # self._client = InfluxDBClient(self.host, self.port, self.username, self.password, self.database_name)
        return

    def post_points_all(self, point_data):
        # point_data should contain all point data
        # push to histories
        return

    def post_points_single(self, point_data):
        # This will potentially be used for COV events
        return