## Copyright (C) 2009 Roberto Cavada

from gi.repository import Gtk

import _importer

from gtkmvc3 import Model
from gtkmvc3 import View
from gtkmvc3 import Controller


class MyView (View):
    builder = "example.ui"
    top = "window1"

    def enable_rb2(self, flag):
        """enables/disables all widgets regarding rb2"""
        self['table1'].set_sensitive(flag)


class MyModel(Model):
    use_rb1 = True
    option1 = 5
    option2 = "text for option2"

    __observables__ = ("use_rb1", "option1", "option2")

    def do_action(self):
        print("model performs action:",
              self.use_rb1, self.option1, self.option2)


class MyController(Controller):

    def register_adapters(self):
        self.adapt("use_rb1", "rb1")
        self.adapt("option1")
        self.adapt("option2")

    # signals handling
    def on_button_action_clicked(self, button):
        self.model.do_action()

    def on_window1_delete_event(self, w, e):
        Gtk.main_quit()
        return False

    # observable properties notifications
    def property_use_rb1_value_change(self, model, old, new):
        self.view.enable_rb2(not new)

if "__main__" == __name__:
    m = MyModel()
    v = MyView()
    c = MyController(m, v)
    Gtk.main()
