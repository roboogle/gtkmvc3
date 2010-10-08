"""
Like adapter3.py but using dict property.
"""
import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters import StaticContainerAdapter

import gtk


class MyView (View):
    glade = "adapters.glade"
    top = "window4"


class MyModel (Model):
    box = {
        'en4' : 0,
        'lbl4' : 1,
        'sb4' : 2}
    __observables__ = ("box",)

    def __init__(self):
        Model.__init__(self)
        return
    pass

import random
class MyCtrl (Controller):

    def on_button4_clicked(self, button):
        k = random.choice(self.model.box.keys())
        self.model.box[k] += 1
        return
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

a1 = StaticContainerAdapter(m, "box")
a1.connect_widget(map(lambda x: v[x], "en4 lbl4 sb4".split()), 
                  setters = {'lbl4': lambda w, v: w.set_markup("<big>Val: <b>%d</b></big>" % v),})


gtk.main()



