"""
Test shows a variety of widgets with at least two per model property. Changing
any should affect others.
"""
import _importer
from gtkmvc3 import Model, Controller, View
from gtkmvc3.adapters.basic import Adapter

from gi.repository import Gtk, Gdk


class MyView (View):
    builder = "adapter11.ui"
    top = "window9"


class MyModel (Model):
    expan = True
    toggle = True
    color = Gdk.color_parse("black")
    url = "http://www.google.com"
    spin = 5.0
    __observables__ = ("expan", "toggle", "color", "url", "spin")


class MyCtrl (Controller):
    def register_view(self, view):
        view.get_top_widget().connect('delete-event', Gtk.main_quit)

    def register_adapters(self):

        # labels

        self.adapt("expan", "label10")

        ad = Adapter(self.model, "toggle")
        ad.connect_widget(self.view["label_t1"], setter=lambda w,v: \
                            w.set_markup("<big><b>%i</b></big>" % v))
        self.adapt(ad)
        self.adapt("toggle", "label_t2")
        # Before PyGTK 2.14 this will display the object ID instead of
        # something useful.
        self.adapt("color", "label_t3")
        self.adapt("url", "label_t4")
        self.adapt("spin", "label_t5")

        # controls
        self.adapt("expan", "expander1")
        self.adapt("toggle", "togglebutton1")
        self.adapt("toggle", "checkbutton1")
        self.adapt("color", "colorbutton1")
        self.adapt("url", "linkbutton1")
        self.adapt("spin", "spinbutton2")

        return

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

Gtk.main()
