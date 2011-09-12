def set_visible_function(model, callback, column=0):
    """
    *model* is a :class:`gtk.TreeModelFilter` instance.

    *callback* will be passed an item and must return a boolean.

    *column* is an integer adressing the column that holds items.

    This calls `model.refilter()` so it may take a while.
    """
    model.set_visible_func(
        lambda tree, iter: callback(
            tree.get_value(iter, column)
            )
        )
    model.refilter()

def get_visible_function(predicates, module):
    """
    Returns a callable that takes an *object* and returns a boolean.

    *predicates* a sequence of 3-tuples.

    *module* an object created with `import`.

    Predicates have the following format:
    
    *attribute* a string naming an attribute of *object*.

    *function* a string naming a factory callable in *module*.

    *argument* can be anything. This will be passed to *function* as its
    sole argument. The result must be a callable that takes a value of
    *attribute* and returns a boolean.
    We do this to make the refilter after changing criteria faster.

    The function we return will lazily evaluate the predicates and logically
    combine their results in an AND fashion.
    """
    stable = tuple(
        (getattr(module, factory)(argument), attribute)
        for attribute, factory, argument in predicates
        )
    def visible_function(obj):
        for function, attribute in stable:
            if not function(getattr(obj, attribute)):
                return False
        return True
    return visible_function
