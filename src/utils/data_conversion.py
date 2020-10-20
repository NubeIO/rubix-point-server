class DataConversion:
    def bool_to_int(self, _val: bool) -> int:
        out = int(_val == True)
        return out
