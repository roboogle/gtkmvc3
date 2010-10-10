"""
Test shows a button and an arrow. Pressing the button should rotate the arrow
90 degrees clockwise.
"""
import _importer
from gtkmvc import Model, Controller, View

import gtk


class MyView (View):
    glade = "adapters.glade"
    top = "window8"


class MyModel (Model):
    dir = gtk.ARROW_UP
    __observables__ = ("dir",)

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):

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
v = MyView()
c = MyCtrl(m, v)

gtk.main()



