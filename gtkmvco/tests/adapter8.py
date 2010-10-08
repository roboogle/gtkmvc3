"""
Like adapter3.py but having StaticContainerAdapter created by Controller.
"""
import _importer
from gtkmvc import Model, Controller, View

import gtk


class MyView (View):
    glade = "adapters.glade"
    top = "window3"


class MyModel (Model):
    box = [0,1,2]
    __observables__ = ("box",)

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):

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
v = MyView()
c = MyCtrl(m, v)

gtk.main()



