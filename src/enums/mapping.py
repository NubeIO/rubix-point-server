import enum


class MapType(enum.Enum):
    GENERIC = 'Generic'


class MappingState(enum.Enum):
    MAPPED = 'Mapped',
    BROKEN = 'Broken'
