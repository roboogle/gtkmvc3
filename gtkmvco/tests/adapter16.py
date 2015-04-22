"""
Test shows a button, a list and an entry. The entry should always reflect the
list selection. The button should change a random list item.

This is a real-world example of dot-notation Adapters with automatic intermediate
observing.
"""

import random
import re

from gi.repository import Gtk

import _importer
import gtkmvc3

class Selection(gtkmvc3.adapters.basic.Adapter):
    def __init__(self, model, prop_name, empty):
        if not getattr(model, prop_name):
            setattr(model, prop_name, empty)
        self.empty_model = empty
        gtkmvc3.adapters.basic.Adapter.__init__(self, model, prop_name)

    def connect_widget(self, treeview):
        sel = treeview.get_selection()
        def getter(s):
            tree_model, iter = s.get_selected()
            if iter:
                return tree_model[iter][0]
            else:
                return self.empty_model
        def setter(s, v):
            pass
        gtkmvc3.adapters.basic.Adapter.connect_widget(self, sel,
            getter, setter, "changed")

class Person(gtkmvc3.Model):
    name = None
    __observables__ = ("name",)

    def __init__(self, name):
        gtkmvc3.Model.__init__(self)
        self.name = name

    def lengthen(self):
        self.name = re.sub(r'(?i)([aeiou])', r'\1\1', self.name, 1).capitalize()

class AddressBook(gtkmvc3.Model):
    selected = None
    __observables__ = ("selected",)

    def __init__(self):
        gtkmvc3.Model.__init__(self)
        self.tree_model = Gtk.ListStore(object)

    def add(self, person):
        person.register_observer(self)
        self.tree_model.append([person])

    def property_name_value_change(self, person, old, new):
        for r in self.tree_model:
            if r[0] is person:
                self.tree_model.row_changed(r.path, r.iter)

    def doodle(self):
        r = random.choice(self.tree_model)
        r[0].lengthen()

class View(gtkmvc3.View):
    def __init__(self):
        gtkmvc3.View.__init__(self)

        w = self['window'] = Gtk.Window()
        b = self['touch'] = Gtk.Button("Doodle")
        t = self['tree'] = Gtk.TreeView()
        e = self['name'] = Gtk.Entry()
        v = Gtk.VBox()
        v.add(b)
        v.add(t)
        v.add(e)
        w.add(v)
        w.set_title("Inspect")
        w.set_default_size(200, 100)
        w.show_all()

class Controller(gtkmvc3.Controller):
    def register_view(self, view):
        view['window'].connect('delete-event', self.on_window_delete_event)
        view['touch'].connect('clicked', self.on_button_clicked)

    def register_adapters(self):
        a = Selection(self.model, "selected", Person(""))
        a.connect_widget(self.view["tree"])
        self.adapt(a)

        self.adapt("selected.name", "name")

        self.setup_columns()

    def setup_columns(self):
        t = self.view['tree']
        t.set_model(self.model.tree_model)

        r = Gtk.CellRendererText()
        c = Gtk.TreeViewColumn('Name', r)
        c.set_cell_data_func(r, self.render)
        t.append_column(c)

    def render(self, column, cell, model, iter, data=None):
        cell.set_property("text", model[iter][0].name)

    def on_window_delete_event(self, window, event):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        self.model.doodle()

m = AddressBook()
m.add(Person("John"))
m.add(Person("Julia"))
m.add(Person("Aron"))
v = View()
c = Controller(m, v)

Gtk.main()
