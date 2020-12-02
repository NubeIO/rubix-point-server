import enum


class HistoryType(enum.Enum):
    COV = 0,
    INTERVAL = 1


class MathOperation(enum.Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3
    BOOL_INVERT = 4
