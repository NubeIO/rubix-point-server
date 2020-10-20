class DataValidation:
    # is null
    def is_none(self, _val) -> bool:
        if _val is None:
            return True
        else:
            return False

    def is_empty(self, _val) -> bool:
        if not _val:
            return True
        else:
            return False

    def type_check(self, _val, expected) -> bool:
        """
        Check data type
        :param _val: value to check
        :param expected: expected type: bool, int, float, str
        :return: bool
        """
        if expected == "bool":
            if isinstance(_val, bool):
                return True
            else:
                return False
        elif expected == "int":
            if isinstance(_val, int):
                return True
            else:
                return False
        elif expected == "float":
            if isinstance(_val, float):
                return True
            else:
                return False
        elif expected == "str":
            if isinstance(_val, str):
                return True
            else:
                return False
