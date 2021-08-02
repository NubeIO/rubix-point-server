import enum


class HistoryType(enum.Enum):
    COV = 0,
    INTERVAL = 1
    COV_AND_INTERVAL = 2


class GenericPointType(enum.Enum):
    INT = 1
    FLOAT = 2
    STRING = 3
    BOOL = 4



