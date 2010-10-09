"""
Like adapter7.py but using GtkBuilder.
"""
import _importer
from gtkmvc import Model, Controller, View

import gtk

class MyView(View):
    builder = "adapter19.ui"
    top = "window7"

class MyModel(Model):
    en1 = 10.0
    __observables__ = ("en1",)

class MyCtrl (Controller):

    def register_adapters(self):
        self.adapt()
        self.adapt('en1', 'label7')        
    
    def on_button7_clicked(self, button):
        self.model.en1 += 1
    
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()
