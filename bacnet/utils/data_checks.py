# is null
def is_none(_val) -> bool:
    if _val is None:  # The variable
        return True
    else:
        return False


def is_empty(_val) -> bool:
    if not val:
        return True
    else:
        return False


def is_int(_val):
    try:
        int(_val)
        return True
    except:
        return False


# test
test = True
if not test:
    exit()
print("test is_none")
val = None
print(is_none(val))
val = " "
print(is_none(val))
val = "123"
print(is_none(val))
val = 123
print(is_none(val))

print("test is_empty")
val = None
print(is_empty(val))
val = ""
print(is_empty(val))
val = "123"
print(is_empty(val))
val = 123
print(is_empty(val))

print("test is_numeric")
val = None
print(is_int(val))
val = ""
print(is_int(val))
val = "123"
print(is_int(val))
val = 123
print(is_int(val))
