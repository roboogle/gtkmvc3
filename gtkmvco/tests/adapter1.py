import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter
from gtkmvc import observable

import gtk



class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window1")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'en1' : 10.0,
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def on_button1_clicked(self, button):
        self.model.en1 += 1
        return
    
    pass

# ----------------------------------------------------------------------

def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()
    
m = MyModel()
c = MyCtrl(m)
v = MyView(c)

a1 = Adapter(m, "en1",
             prop_read=lambda v: v/2.0, prop_write=lambda v: v*2,
             value_error=myerr)
a1.connect_widget(v["entry1"])

a2 = Adapter(m, "en1")
a2.connect_widget(v["label1"], wid_setter=lambda w,v: w.set_markup("<big><b>%.2f</b></big>" % v))

gtk.main()



