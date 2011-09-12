import datetime

def lt(y):
    """
    For str this is equivalent to y.__gt__, but int doesn't have those slots.
    """
    return lambda x: x < y

def gt(y):
    return lambda x: x > y

def ne(y):
    return lambda x: x != y

def gtif(y):
    """
    Like gt but True if operand is None.
    """
    return lambda x: not x or x > y

def contains(y):
    """
    Case-insensitive substring search.
    """
    y = y.lower()
    return lambda x: y in x.lower()

def eqdate(y):
    """
    Like eq but compares datetime with y,m,d tuple.
    Also accepts magic string 'TODAY'.
    """
    y = datetime.date.today() if y == 'TODAY' else datetime.date(*y)
    return lambda x: x == y
