import json
import re
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
    return datetime.utcnow()


def validate_json(value: str):
    """
    Rules for valid json:
    - force all json to be lower case
    - if there is a gap add an underscore
    - no special characters
    """
    objects = json.loads(value)
    return_value: dict = {}
    for obj in objects:
        clean_obj: str = obj.replace(" ", "_")
        clean_obj = re.sub('[^A-Za-z0-9_]+', '', clean_obj)
        return_value[clean_obj] = objects[obj]
    return json.dumps(return_value)
