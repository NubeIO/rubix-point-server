from datetime import datetime
class ModelUtils:
    @staticmethod
    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            attr = getattr(row, column.name)
            if isinstance(attr, (int, str, bool, float)):
                d[column.name] = attr
            else:
                d[column.name] = str(attr)
        return d

    @staticmethod
    def row2dict_default(row):
        d = {}
        for column in row.__table__.columns:
            attr = getattr(row, column.name)
            d[column.name] = attr
        return d


def get_datetime() -> datetime:
    return datetime.now()


def datetime_to_str(datetime_obj: datetime or None) -> str:
    if datetime_obj is not None:
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
