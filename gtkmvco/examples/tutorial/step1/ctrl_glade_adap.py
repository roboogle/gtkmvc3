# Author: Roberto Cavada, Copyright 2007
#
# This is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# These examples are distributed in the hope that they will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.


# This is file ctrl_glade_adapt.py
import _importer
from gtkmvc3 import Controller
from gi.repository import Gtk


class MyControllerAdap (Controller):

    def register_adapters(self):
        # This is a simple adapter
        #self.adapt("counter", "label")

        # This is for a custom adapter
        from gtkmvc3 import adapters
        a = adapters.Adapter(self.model, "counter")
        a.connect_widget(self.view['label'],
                         setter=lambda w,v:
                         w.set_markup("<big>counter=<b>%02d</b></big>" % v))
        self.adapt(a)

    # signals:
    def on_main_window_delete_event(self, w, e):
        Gtk.main_quit()
        return False

    def on_button_clicked(self, button):
        self.model.counter += 1  # changes the model
