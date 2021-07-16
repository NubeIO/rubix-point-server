import enum


class MapType(enum.Enum):
    GENERIC = 'Generic'
    BACNET = 'Bacnet'


class MappingState(enum.Enum):
    MAPPED = 'Mapped',
    BROKEN = 'Broken'
