"""
Test shows an entry and a spinner. Changing the latter should print a
notification. Closing the window should exit the program.
"""

from gi.repository import Gtk
import _importer
import gtkmvc3


# MyModel.py
class MyModel (gtkmvc3.Model):
    name = "Roberto"
    age = 0
    __observables__ = ["name", "age" ]


# MyCtrl.py
class MyCtrl (gtkmvc3.Controller):

    def register_adapters(self):
        # good time to create adapters
        self.adapt("name")
        self.adapt("age")

    def register_view(self, view):
        gtkmvc3.Controller.register_view(self, view)
        view['window'].connect('delete-event', Gtk.main_quit)


# MyView.py
class MyView (gtkmvc3.View):
    def __init__(self):
        super(MyView, self).__init__()
        self.__create_manual_widgets()
        return

    def __create_manual_widgets(self):
        self['window'] = Gtk.Window()
        self['window'].set_title("A damned small example")
        t = Gtk.Table(rows=2, columns=2)
        t.set_row_spacings(12)
        t.set_col_spacings(6)

        t.attach(Gtk.Label("Name:"), 0, 1, 0, 1)
        t.attach(Gtk.Label("Age:"), 0, 1, 1, 2)
        self['entry_name'] = Gtk.Entry()
        t.attach(self['entry_name'], 1, 2, 0, 1)
        self['sb_age'] = Gtk.SpinButton(
            adjustment=Gtk.Adjustment(0, 0, 100, step_incr=1))
        t.attach(self['sb_age'], 1, 2, 1, 2)

        self['window'].add(t)
        self['window'].show_all()


class MyObserver (gtkmvc3.Observer):
    def property_age_value_change(self, model, old, new):
        print("age changed from %d to %d" % (old, new))




# main.py
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

o = MyObserver(m)

Gtk.main()
