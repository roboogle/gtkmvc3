"""
Test shows an entry and a spinner. Changing the latter should print a
notification. Closing the window should exit the program.

WARNING tested on GTK 2.18.2 because with GTK 2.10.4 SpinButton emits "changed"
twice as often! The first notification always resets the value to zero.
"""
# MyModel.py
import _importer
import gtkmvc
class MyModel (gtkmvc.Model):
    name = "Roberto"
    age = 0
    __observables__ = ["name", "age" ]

    pass # end of class


# MyCtrl.py
import gtkmvc
import gtk
class MyCtrl (gtkmvc.Controller):

    def register_adapters(self):
        # good time to create adapters
        self.adapt("name")
        self.adapt("age")
        return

    def register_view(self, view):
        gtkmvc.Controller.register_view(self, view)
        view['window'].connect('delete-event', gtk.main_quit)
        return

    pass # end of class

# MyView.py
import gtkmvc
import gtk
class MyView (gtkmvc.View):
    def __init__(self):
        super(MyView, self).__init__()
        self.__create_manual_widgets()
        return

    def __create_manual_widgets(self):
        self['window'] = gtk.Window()
        self['window'].set_title("A damned small example")
        t = gtk.Table(rows=2, columns=2)
        t.set_row_spacings(12)
        t.set_col_spacings(6)

        t.attach(gtk.Label("Name:"), 0, 1, 0, 1)
        t.attach(gtk.Label("Age:"), 0, 1, 1, 2)
        self['entry_name'] = gtk.Entry()
        t.attach(self['entry_name'], 1, 2, 0, 1)
        self['sb_age'] = gtk.SpinButton(gtk.Adjustment(0, 0, 100, step_incr=1))
        t.attach(self['sb_age'], 1, 2, 1, 2)
        
        self['window'].add(t)
        self['window'].show_all()
        return

    pass # end of class

class MyObserver (gtkmvc.Observer):
    def property_age_value_change(self, model, old, new):
        print "age changed from %d to %d" % (old, new)
        return
    pass # end of class

    
    

# main.py
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

o = MyObserver(m)

gtk.main()
