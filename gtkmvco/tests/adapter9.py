import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.containers import StaticContainerAdapter

import gtk


class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window8")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'dir' : gtk.ARROW_UP,
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
        self.adapt("dir")
        return

    def on_button5_clicked(self, button):
        vals = [gtk.ARROW_UP, gtk.ARROW_RIGHT, gtk.ARROW_DOWN, gtk.ARROW_LEFT]
        self.model.dir = vals[(vals.index(self.model.dir)+1) % len(vals)]
        return
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
c = MyCtrl(m)
v = MyView(c)

gtk.main()



