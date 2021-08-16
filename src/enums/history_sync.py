import enum


class HistorySyncType(enum.Enum):
    POSTGRES = 'Postgres',
    INFLUX = 'Influx'
