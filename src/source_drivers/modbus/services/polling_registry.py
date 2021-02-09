from src.utils import Singleton


class PoolingRegistry(metaclass=Singleton):

    def __init__(self):
        self.__pooling_stats = {}

    def polling_stats(self):
        return self.__pooling_stats

    def update(self, stat):
        if stat:
            self.__pooling_stats.update(**stat)
