import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter

import gtk



class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window7")
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
c = MyCtrl(m)
v = MyView(c)

gtk.main()



