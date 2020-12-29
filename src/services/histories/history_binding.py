from abc import abstractmethod


class HistoryBinding:

    @abstractmethod
    def connect(self):
        raise Exception("History Binding connect not implemented")

    @abstractmethod
    def sync(self):
        raise Exception("History Binding sync not implemented")
