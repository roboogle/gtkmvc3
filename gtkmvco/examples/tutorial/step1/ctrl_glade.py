# Author: Roberto Cavada, Copyright 2004-2015
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

import _importer
from gtkmvc3 import Controller
from gi.repository import Gtk

class MyController (Controller):
    """Customized controller.

    The controller carries out two tasks:
       - When view's button is clicked, increments model property
         'counter'
       - When the property changes, updates the view's label text
         correspondently. This means that the controller is
         an observer for property 'counter' as well."""

    def register_view(self, view):
        """This method is called by the view, that calls it when it is
        ready to register itself. Here we connect the 'pressed' signal
        of the button with a controller's method. Signal 'destroy'
        for the main window is handled as well."""

        # initializes the text of label:
        self.view.set_text("%d" % self.model.counter)

    # signals:
    def on_main_window_delete_event(self, w, e):
        Gtk.main_quit()
        return False

    def on_button_clicked(self, button):
        self.model.counter += 1  # changes the model

    # observable properties:
    @Controller.observe("counter", assign=True)
    def counter_value_change(self, model, prop_name, info):
        self.view.set_text("%d" % info.new)
        print("Property 'counter' changed value from %d to %d" \
              % (info.old, info.new))
