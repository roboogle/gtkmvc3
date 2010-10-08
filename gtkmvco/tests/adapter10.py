"""
Test shows a calendar and a button. Pressing the button should print the
selected date with the time of launching the program.
"""
import _importer
from gtkmvc import Model, Controller, View

import gtk


class MyView (View):
    glade = "adapters.glade"
    top = "window5"

import datetime
class MyModel (Model):
    data = datetime.datetime.today()
    __observables__ = ("data",)

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):

    def register_adapters(self):
        self.adapt("data", "calendar")
        return

    def on_button8_clicked(self, button): print self.model.data
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()



