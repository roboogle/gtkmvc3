"""
Test shows an entry and a label. Changing the entry should adjust the label
only for even numbers, otherwise it will turn red until a valid change.

This tests the new prop_write semantics which no longer attempt a cast.
"""

import gtk

import _importer
import gtkmvc

class Even(gtkmvc.adapters.basic.Adapter):
    """
    We have to subclass to access _wid.
    We may get called before connect_widget, so _wid may be None.
    """
    def __init__(self, model, prop_name):
        color = gtk.gdk.color_parse("#FF7E7E")
        def prop_read(v):
            if self._wid:
                self._wid.modify_base(gtk.STATE_NORMAL, None)
            return str(v)
        def prop_write(v):
            v = int(v)
            if v % 2 > 0:
                raise ValueError("Evil Experiment")
            elif self._wid:
                self._wid.modify_base(gtk.STATE_NORMAL, None)
            return v
        def value_error(self, prop_name, v):
            if self._wid:
                self._wid.modify_base(gtk.STATE_NORMAL, color)
        gtkmvc.adapters.basic.Adapter.__init__(self, model, prop_name,
            prop_read, prop_write, value_error)

class Animal(gtkmvc.Model):
    legs = 2
    __observables__ = ("legs",)

class Laboratory(gtkmvc.View):
    def __init__(self):
        gtkmvc.View.__init__(self)

        w = self['window'] = gtk.Window()
        e = self['entry_legs'] = gtk.Entry()
        l = self['label_legs'] = gtk.Label()
        b = gtk.VBox()
        b.pack_start(e)
        b.pack_start(l)
        w.add(b)
        w.set_title("How many legs?")
        w.set_default_size(300, 150)
        w.show_all()

class Scientist(gtkmvc.Controller):
    def register_view(self, view):
        view['window'].connect('delete-event', self.on_window_delete_event)

    def register_adapters(self):
        self.adapt("legs", "label_legs")
        a = Even(self.model, "legs")
        a.connect_widget(self.view["entry_legs"])
        self.adapt(a)
    
    def on_window_delete_event(self, window, event):
        gtk.main_quit()

m = Animal()
v = Laboratory()
c = Scientist(m, v)

gtk.main()
