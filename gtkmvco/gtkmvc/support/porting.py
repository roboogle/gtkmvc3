


# This was made by Martijn Pieters
# See http://www.zopatista.com/python/2014/03/14/cross-python-metaclasses/
def with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        # clean out class body
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)

    return decorator
