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
