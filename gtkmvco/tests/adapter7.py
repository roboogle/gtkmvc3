"""
Test shows an entry, a label, and two buttons. Undo is not hooked up. Pressing
the other button should increment the entry by one. The label should show the
same value.
"""
import _importer
from gtkmvc import Model, Controller, View

import gtk



class MyView (View):
    glade = "adapters.glade"
    top = "window7"


class MyModel (Model):
    en1 = 10.0
    __observables__ = ("en1",)

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):

    def register_adapters(self):
        self.adapt('en1', 'label7')        
        self.adapt('en1')        
        return
    
    def on_button7_clicked(self, button):
        self.model.en1 += 1
        return
    
    pass

# ----------------------------------------------------------------------

    
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()



