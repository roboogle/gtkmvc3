"""
Test shows a label and several buttons. Either button should change the label.
"""

import time

from gi.repository import Gtk

import _importer
import gtkmvc3

class Model(gtkmvc3.Model):
    next = None
    __observables__ = ("next",)

    def __init__(self):
        gtkmvc3.Model.__init__(self)
        self.next = time.time()


class View(gtkmvc3.View):
    def __init__(self):
        gtkmvc3.View.__init__(self)

        w = self['window'] = Gtk.Window()
        l = self['time'] = Gtk.Label()
        b = Gtk.VBox()
        b.add(l)
        for i in range(3):
            i = str(i)
            p = self[i] = Gtk.Button(i)
            b.add(p)
        w.add(b)
        w.set_title("Click to change")
        w.set_default_size(200, 100)
        w.show_all()


class Controller(gtkmvc3.Controller):
    def register_view(self, view):
        view['window'].connect('delete-event', self.on_window_delete_event)
        for i in range(3):
            i = str(i)
            view[i].connect('clicked', self.on_button_clicked)

    def register_adapters(self):
        self.adapt("next.next.next", "time")

    def on_window_delete_event(self, window, event):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        if button is self.view["2"]:
            self.model.next.next.next = time.time()
        elif button is self.view["1"]:
            m = Model()
            self.model.next.next = m
        elif button is self.view["0"]:
            m = Model()
            m.next = Model()
            self.model.next = m

m = Model()
m.next = Model()
m.next.next = Model()
v = View()
c = Controller(m, v)

Gtk.main()
