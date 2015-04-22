"""
Test shows a button and an arrow. Pressing the button should rotate the arrow
90 degrees clockwise.
"""
import _importer
from gtkmvc3 import Model, Controller, View

from gi.repository import Gtk


class MyView (View):
    builder = "adapter9.ui"
    top = "window8"


class MyModel (Model):
    dir = Gtk.ArrowType.UP
    __observables__ = ("dir",)


class MyCtrl (Controller):

    def register_view(self, view):
        view.get_top_widget().connect('delete-event', Gtk.main_quit)

    def register_adapters(self):
        self.adapt("dir")

    def on_button5_clicked(self, button):
        vals = [Gtk.ArrowType.UP, Gtk.ArrowType.RIGHT,
                Gtk.ArrowType.DOWN, Gtk.ArrowType.LEFT]
        self.model.dir = vals[(vals.index(self.model.dir)+1) % len(vals)]

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

Gtk.main()
