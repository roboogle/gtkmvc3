"""
Test shows an entry and a button. Pressing the button should increment the
entry by one. Changing the entry manually to a value > 10 will print a message,
doing it by pressing the button will raise ValueError in the signal handler.
"""
import _importer
from gtkmvc import Model, Controller, View, Observable
from gtkmvc.adapters.basic import UserClassAdapter

import gtk


class UserClass (Observable):
    def __init__(self, max_val):
        Observable.__init__(self)
        self.x = 0
        self.max_val = max_val
        return

    @Observable.observed
    def set_x(self, v):
        if v > self.max_val:
            raise ValueError("x cannot be greater than %d" % self.max_val)
        self.x=v
        return
        
    def get_x(self): return self.x
    pass


class MyView (View):
    glade = "adapters.glade"
    top = "window2"


class MyModel (Model):
    x = UserClass(10)
    __observables__ = ("x",)


class MyCtrl (Controller):

    def on_button2_clicked(self, button):
        self.model.x.set_x(self.model.x.get_x() + 1)
        return
    
    pass

# ----------------------------------------------------------------------

def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()
    
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

a1 = UserClassAdapter(m, "x", "get_x", "set_x", value_error=myerr)
a1.connect_widget(v["en2"])

m.x.set_x(5)

gtk.main()



