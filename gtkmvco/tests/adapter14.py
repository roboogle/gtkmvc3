"""
Test shows an entry and a label. Changing the entry should adjust the label
only for even numbers, otherwise it will turn red until a valid change.

This tests the new prop_write semantics which no longer attempt a cast.
"""

from gi.repository import Gtk
from gi.repository import Gdk

import _importer
import gtkmvc3


class Even(gtkmvc3.adapters.basic.Adapter):
    """
    We have to subclass to access _wid.
    We may get called before connect_widget, so _wid may be None.
    """
    def __init__(self, model, prop_name):

        Even._set_css()

        def prop_read(v):
            if self._wid:
                self._wid.set_name("Entry_ok")
            return str(v)

        def prop_write(v):
            v = int(v)
            if v % 2 != 0:
                raise ValueError("Evil Experiment")
            elif self._wid:
                self._wid.set_name("Entry_ok")
            return v

        def value_error(self, prop_name, v):
            if self._wid:
                self._wid.set_name("Entry_fail")

        gtkmvc3.adapters.basic.Adapter.__init__(self, model, prop_name,
                                               prop_read, prop_write,
                                               value_error)

    @staticmethod
    def _set_css():
        sp = Gtk.CssProvider()

        css = b"""
#Entry_ok {
        }
#Entry_fail {
        background-color: #908080;
        color: #FF0000;
        font-weight: bold;
        }
        """
        sp.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            sp,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class Animal(gtkmvc3.Model):
    legs = 2
    __observables__ = ("legs",)


class Laboratory(gtkmvc3.View):
    def __init__(self):
        gtkmvc3.View.__init__(self)

        w = self['window'] = Gtk.Window()
        e = self['entry_legs'] = Gtk.Entry()
        l = self['label_legs'] = Gtk.Label()
        b = Gtk.VBox()
        b.add(e)
        b.add(l)
        w.add(b)
        w.set_title("How many legs?")
        w.set_default_size(300, 150)
        w.show_all()


class Scientist(gtkmvc3.Controller):
    def register_view(self, view):
        view['window'].connect('delete-event', self.on_window_delete_event)

    def register_adapters(self):
        self.adapt("legs", "label_legs")

        a = Even(self.model, "legs")
        a.connect_widget(self.view["entry_legs"])
        self.adapt(a)

    def on_window_delete_event(self, window, event):
        Gtk.main_quit()


m = Animal()
v = Laboratory()
c = Scientist(m, v)

Gtk.main()
