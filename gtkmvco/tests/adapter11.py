import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter

import gtk


class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window9")
        return
    pass

import datetime
class MyModel (Model):
    __properties__ = {
        'expan' : True,
        'toggle' : True,
        'color' : gtk.gdk.color_parse("black"),
        'url' : "http://www.google.com",
        'spin' : 5.0,
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def register_adapters(self):
        
        # labels

        self.adapt("expan", "label10")
        
        ad = Adapter(self.model, "toggle")
        ad.connect_widget(self.view["label_t1"], setter=lambda w,v: \
                            w.set_markup("<big><b>%i</b></big>" % v))
        self.adapt(ad)
        self.adapt("toggle", "label_t2")
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

    pass

# ----------------------------------------------------------------------

m = MyModel()
c = MyCtrl(m)
v = MyView(c)

gtk.main()



