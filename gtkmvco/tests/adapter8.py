import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.containers import StaticContainerAdapter

import gtk


class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window3")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'box' : [0,1,2]
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
        self.adapt("box", "hbox1")
        return

    def on_button3_clicked(self, button):
        import random
        self.model.box[random.randint(0,2)] += 1
        return
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
c = MyCtrl(m)
v = MyView(c)

gtk.main()



