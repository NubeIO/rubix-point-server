class DataHelpers:
    def num_round(self, _val: float, places: int) -> float:
        if places == 0:
            out = "{:.0f}".format(_val)
            return out
        else:
            return round(_val, places)

    def limit(self, _val: int, _min: int, _max: int) -> int:
        if _val <= _min:
            _val = _min
            return _val
        elif _val >= _max:
            _val = _max
            return _val
        else:
            return _val