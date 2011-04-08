import gtkmvc

class Intermediate(gtkmvc.Observer):
    def __init__(self, model, path, adapter):
        """
        *model* is an instance.

        *path* is a list of strings, with the first naming a property of
        *model*. Its value must have a property named like the second string,
        and so on.

        *adapter* is an instance. Its widget will be updated every time a
        property in *path* changes. Currently this only covers assignment.
        """
        self.model = model
        self.prop_name = path[0]
        self.path = path[1:]
        self.adapter = adapter
        self.next = None

        gtkmvc.Observer.__init__(self)
        self.observe(self.update_widget, self.prop_name, assign=True)
        self.observe_model(model)

        self.create_next()

    def create_next(self):
        if self.path:
            self.next = Intermediate(getattr(self.model, self.prop_name),
                self.path, self.adapter)

    def delete_next(self):
        if self.next:
            self.next.delete()
            self.next = None

    def delete(self):
        self.relieve_model(self.model)
        self.delete_next()

    def update_widget(self, model, prop_name, info):
        self.delete_next()
        self.create_next()
        model = info.new
        for prop_name in self.path:
            model = getattr(model, prop_name)
        # Break encapsulation to change the model of our adapter.
        self.adapter.relieve_model(model)
        self.adapter._model = model
        self.adapter.observe_model(model)
        self.adapter.update_widget()

def adapt(model, prop_name, view, widget_name=None):
    """
    *model* is an instance.

    *prop_name* is a string which may contain dots to indicate a path.

    *view* is an instance.

    *widget_name* is a string. It has to match exactly.
    If not given, the last part of the path is used.

    .. note::
       This method can be replaced by adding a single line to
       Adapter._connect_model
    """
    adapter = gtkmvc.adapters.basic.Adapter(model, prop_name)
    path = prop_name.split('.')
    if len(path) > 1:
        Intermediate(model, path[:-1], adapter)
    adapter.connect_widget(view[widget_name or path[-1]])
    return adapter
