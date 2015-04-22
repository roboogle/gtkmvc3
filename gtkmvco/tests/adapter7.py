"""
Test shows an entry, a label, and two buttons. Undo is not hooked up. Pressing
the other button should increment the entry by one. The label should show the
same value.
"""
import _importer
from gtkmvc3 import Model, Controller, View

from gi.repository import Gtk


class MyView (View):
    builder = "adapter7.ui"
    top = "window7"


class MyModel (Model):
    en1 = 10.0
    __observables__ = ("en1",)

    def __init__(self):
        Model.__init__(self)


class MyCtrl (Controller):

    def register_view(self, view):
        view.get_top_widget().connect('delete-event', Gtk.main_quit)

    def register_adapters(self):
        self.adapt('en1', 'label7')
        self.adapt('en1')

    def on_button7_clicked(self, button):
        self.model.en1 += 1

# ----------------------------------------------------------------------


m = MyModel()
v = MyView()
c = MyCtrl(m, v)

Gtk.main()
