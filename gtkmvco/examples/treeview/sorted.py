import gtk

import _importer
import gtkmvc

from sorting import *

class Person(gtkmvc.Model):
    name = ''
    age = 0
    __observables__ = ('name', 'age')

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        def add(name, age):
            p = Person()
            p.name = name
            p.age = age
            view['liststore'].append([p])
        add("Adam", 30)
        add("Zachary", 30)
        add("Berta", 20)
        add("Yolanda", 20)

    def register_adapters(self):
        self.setup_columns()

        s = self.view['sorting'] = SortingView()
        s.set_labels(dict(name="Nome", age="Eta"))
        s.set_order([
            {'reverse': False, 'key': 'age'},
            {'reverse': False, 'key': 'name'},
            ])
        self.view['frame'].add(s)

    def on_button__clicked(self, widget):
        set_sort_function(
            self.view['treemodelsort'],
            get_sort_function(self.view['sorting'].get_order())
            )

    def on_window__delete_event(self, widget, event):
        gtk.main_quit()

m = gtkmvc.Model()
v = gtkmvc.View(builder='sorted.ui')
c = Controller(m, v, handlers='class')

gtk.main()
