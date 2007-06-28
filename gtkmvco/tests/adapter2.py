import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import UserClassAdapter
from gtkmvc import observable

import gtk


class UserClass (observable.Observable):
    def __init__(self, max_val):
        observable.Observable.__init__(self)
        self.x = 0
        self.max_val = max_val
        return

    @observable.observed
    def set_x(self, v):
        if v > self.max_val:
            raise ValueError("x cannot be greater than %d" % self.max_val)
        self.x=v
        return
        
    def get_x(self): return self.x
    pass


class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window2")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'x'   : UserClass(10), 
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def on_button2_clicked(self, button):
        self.model.x.set_x(self.model.x.get_x() + 1)
        return
    
    pass

# ----------------------------------------------------------------------

def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()
    
m = MyModel()
c = MyCtrl(m)
v = MyView(c)

a1 = UserClassAdapter(m, "x", "get_x", "set_x", value_error=myerr)
a1.connect_widget(v["en2"])

m.x.set_x(5)

gtk.main()



