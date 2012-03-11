import gtk

def _normalize(cmp):
    # TODO use bit-shift?
    if cmp < 0:
        return -1
    elif cmp > 0:
        return 1
    else:
        return 0

def set_sort_function(sortable, callback, column=0):
    """
    *sortable* is a :class:`gtk.TreeSortable` instance.

    *callback* will be passed two items and must return a value like
    the built-in `cmp`.

    *column* is an integer adressing the column that holds items.

    This will re-sort even if *callback* is the same as before.

    .. note::
       When sorting a `ListStore` without a `TreeModelSort` you have to call
       `set_sort_column_id(-1, gtk.SORT_ASCENDING)` once, *after* this.
    """
    sortable.set_default_sort_func(
        lambda tree, itera, iterb: _normalize(callback(
            tree.get_value(itera, column),
            tree.get_value(iterb, column)
            ))
        )

def get_sort_function(order):
    """
    Returns a callable similar to the built-in `cmp`, to be used on objects.

    Takes a list of dictionaries. In each, 'key' must be a string that is
    used to get an attribute of the objects to compare, and 'reverse' must
    be a boolean indicating whether the result should be reversed.
    """
    stable = tuple((d['key'], -1 if d['reverse'] else 1) for d in order)
    def sort_function(a, b):
        for name, direction in stable:
            v = cmp(getattr(a, name) if a else a, getattr(b, name) if b else b)
            if v != 0:
                return v * direction
        return 0
    return sort_function

class SortingView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        self.set_properties(visible=True, headers_visible=False,
            reorderable=True)

        def row_activated(widget, path, column):
            model = widget.get_model()
            iter = model.get_iter(path)
            reverse = model.get_value(iter, 0)
            model.set_value(iter, 0, not reverse)

        self.connect('row-activated', row_activated)

        def append_column(cls, func):
            r = cls()
            c = gtk.TreeViewColumn(None, r)
            c.set_cell_data_func(r, func)
            self.append_column(c)

        def pixbuf_data(column, renderer, model, iter):
            reverse = model.get_value(iter, 0)
            renderer.set_property('stock-id', gtk.STOCK_SORT_DESCENDING
                if reverse else gtk.STOCK_SORT_ASCENDING)

        append_column(gtk.CellRendererPixbuf, pixbuf_data)
        
        def text_data(column, renderer, model, iter):
            key = model.get_value(iter, 1)
            renderer.set_property('text', self.__labels[key])

        append_column(gtk.CellRendererText, text_data)

    def set_labels(self, labels):
        """
        Takes a dictionary mapping keys to sort by to display labels.
        """
        self.__labels = labels

    def get_order(self):
        """
        Return a list of dicionaries. See `set_order`.
        """
        return [dict(reverse=r[0], key=r[1]) for r in self.get_model()]

    def set_order(self, order):
        """
        Takes a list of dictionaries. Those correspond to the arguments of
        `list.sort` and must contain the keys 'key' and 'reverse' (a boolean).

        You must call `set_labels` before this!
        """
        m = gtk.ListStore(bool, str)
        for item in order:
            m.append(
                (item['reverse'], item['key'])
                )
        # TODO fill with __labels missing in order.
        self.set_model(m)
