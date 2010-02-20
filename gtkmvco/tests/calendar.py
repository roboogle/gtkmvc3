import _importer
from gtkmvc import Model, Controller, View
import gtk

class MyView (View):
    glade = "calendar.glade"
    pass

import datetime
class MyModel (Model):
    data = datetime.datetime.today()
    __observables__ = ('data',)

    def increment(self): self.data += datetime.timedelta(1)
    pass # end of class


class MyCtrl (Controller):

    def register_view(self, view):
        view['window1'].connect('delete-event', gtk.main_quit)
        return
    
    def register_adapters(self):
        self.adapt("data", "calendar")
        return

    def on_button_print_clicked(self, button):
        print self.model.data
        return

    def on_button_inc_clicked(self, button):
        self.model.increment() 
        return
        
    pass # end of class

# ----------------------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()



