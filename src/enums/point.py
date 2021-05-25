import enum


class HistoryType(enum.Enum):
    COV = 0,
    INTERVAL = 1
    COV_AND_INTERVAL = 2


class Sources(enum.Enum):
    OWN = 0,
    MAPPING = 1
