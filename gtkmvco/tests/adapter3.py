"""
Test shows a button and an HBox with three different widgets displaying
numbers. Pressing the button should increment one of the three at random.
The outer two should also be editable.
"""
import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.containers import StaticContainerAdapter

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

import random
class MyCtrl (Controller):

    def on_button3_clicked(self, button):
        self.model.box[random.randint(0,2)] += 1
        return
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

a1 = StaticContainerAdapter(m, "box")
a1.connect_widget(v["hbox1"])


gtk.main()



