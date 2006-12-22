# Author: Roberto Cavada, Copyright 2004
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
from gtkmvc import View
import gtk

# ----------------------------------------------------------------------
class MyViewNoGlade (View):
    """Manually constructed view, without any glade file.

       The view is a window containing a button and a label. The label
       shows the value of a counter contained in the model. Of course
       the controller does the connection. Every time the button is
       pressed, the counter will be incremented."""

    def __init__(self, ctrl):

        # The view here is not constructed from a glade file.
        # Registration is delayed, and widgets are added manually,
        # later.
        View.__init__(self, ctrl, register=False)
    
        # The set of widgets:
        w = gtk.Window()
        h = gtk.VBox()
        l = gtk.Label()
        b = gtk.Button("Press")
        h.pack_start(l)
        h.pack_end(b)
        w.add(h)
        w.show_all()

        # We add all widgets we are interested in retrieving later in
        # the view, by giving them a name. Suppose you need access
        # only to the main window, label and button.  Widgets are
        # added like in a map:
        self['main_window'] = w
        self['label'] = l
        self['button'] = b
        
        # View's registration was delayed, now we can proceed.
        # This will allow the controller to set up all signals
        # connections, and other operations:
        ctrl.register_view(self)
        return

    pass # end of class
# ----------------------------------------------------------------------
