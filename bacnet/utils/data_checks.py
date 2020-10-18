# is null
def is_none(_val) -> bool:
    if _val is None:
        return True
    else:
        return False


def is_empty(_val) -> bool:
    if not _val:
        return True
    else:
        return False


def is_int(_val: int) -> bool:
    try:
        int(_val)
        return True
    except:
        return False


def type_check(_val, expected):
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

# test
# test = True
# if not test:
#     exit()
# print("test is_none")
# val = None
# print(is_none(val))
# val = " "
# print(is_none(val))
# val = "123"
# print(is_none(val))
# val = 123
# print(is_none(val))
#
# print("test is_empty")
# val = None
# print(is_empty(val))
# val = ""
# print(is_empty(val))
# val = "123"
# print(is_empty(val))
# val = 123
# print(is_empty(val))
#
# print("test is_numeric")
# val = None
# print(is_int(val))
# val = ""
# print(is_int(val))
# val = "123"
# print(is_int(val))
# val = 123
# print(is_int(val))
