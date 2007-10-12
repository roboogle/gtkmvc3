#  Author: Roberto Cavada <cavada@irst.itc.it>
#
#  Copyright (c) 2007 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#  02111-1307 USA.
#
#  For more information on pygtkmvc see
#  <http://pygtkmvc.sourceforge.net> or email to the author Roberto
#  Cavada <cavada@irst.itc.it>.  Please report bugs to
#  <cavada@irst.itc.it>.


import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters import StaticContainerAdapter

import gtk

# This example shows how a bunch of widgets can be adapted to an 
# observable property containing a tuple of values.

class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window3")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'box' : [0,1,2]
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass

import random
class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def register_adapters(self):
        a = StaticContainerAdapter(self.model, "box", value_error=myerr)
        a.connect_widget(map(lambda x: self.view[x], "en3 lbl3 sb3".split()), 
                         setters = {'lbl3': lambda w, v: w.set_markup("<big>Val=<b>%d</b></big>" % v),})
        
        return

    def on_button3_clicked(self, button):
        self.model.box[random.randint(0,2)] += 1
        return

    def on_window3_delete_event(self, w, e):
        gtk.main_quit()
        return True

    pass

# ----------------------------------------------------------------------

def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()
    return


m = MyModel()
c = MyCtrl(m)
v = MyView(c)
gtk.main()



