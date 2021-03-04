def rreplace(string: str, old: str, new: str, occurrence: int):
    """
    >>> string
    '1232425'
    >>> rreplace(string, '2', ' ', 2)
    '123 4 5'
    >>> rreplace(string, '2', ' ', 3)
    '1 3 4 5'
    >>> rreplace(string, '2', ' ', 4)
    '1 3 4 5'
    >>> rreplace(string, '2', ' ', 0)
    '1232425'
    """
    list_ = string.rsplit(old, occurrence)
    return new.join(list_)
