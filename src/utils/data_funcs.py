class DataHelpers:
    @staticmethod
    def num_round(_val: float, places: int) -> float:
        if places == 0:
            out = "{:.0f}".format(_val)
            return float(out)
        else:
            return round(_val, places)

    @staticmethod
    def limit(_val: int, _min: int, _max: int) -> int:
        if _val <= _min:
            _val = _min
            return _val
        elif _val >= _max:
            _val = _max
            return _val
        else:
            return _val

    @staticmethod
    def bool_to_int(_val: bool) -> int:
        out = int(_val)
        return out
