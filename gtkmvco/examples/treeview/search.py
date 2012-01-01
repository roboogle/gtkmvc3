"""
Start typing to jump to a row.
"""

import gtk

import _importer
import gtkmvc

class Row(gtkmvc.Model):
    name = ''
    __observables__ = ['name']

def NameStore():
    s = gtk.ListStore(object)
    for name in dir(__builtins__):
        r = Row()
        r.name = name
        s.append([r])
    return s

def search_equal_func(model, column, key, iter, data):
    value = getattr(model.get_value(iter, column), data)
    # Case-sensitive.
    return key not in value

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        view['treeview'].set_model(NameStore())
        view.show()

    def register_adapters(self):
        self.setup_columns()
        self.view['treeview'].set_search_equal_func(search_equal_func, 'name')

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

Controller(
    gtkmvc.Model(),
    gtkmvc.View(builder='search.ui', top='window'),
    handlers='class')
gtk.main()
