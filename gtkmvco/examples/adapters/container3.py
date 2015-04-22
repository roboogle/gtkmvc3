#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2007-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#  02111-1307 USA.
#
#  For more information on gtkmvc3 see
#  <https://github.com/roboogle/gtkmvc3> or email to the author Roberto
#  Cavada <roboogle@gmail.com>.  Please report bugs to
#  <roboogle@gmail.com>.


import _importer
from gtkmvc3 import Model, Controller, View
from gtkmvc3.adapters import StaticContainerAdapter

import gtk

# This example shows how a bunch of widgets can be adapted to an 
# observable property containing a map of integers

class MyView (View):
    glade = "adapters.glade"
    top = "window3"
    pass

class MyModel (Model):
    box = { 'en3' : 0,
            'lbl3' : 1,
            'sb3' : 2 }
    __observables__ = ("box",)
    pass

import random
class MyCtrl (Controller):
    def register_adapters(self):
        a = StaticContainerAdapter(self.model, "box", value_error=myerr)
        a.connect_widget(map(lambda x: self.view[x], "en3 lbl3 sb3".split()), 
                         setters = {'lbl3': lambda w, v: w.set_markup("<big>Val=<b>%d</b></big>" % v),})
        
        return

    def on_button3_clicked(self, button):
        self.model.box[random.choice(self.model.box.keys())] += 1
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
v = MyView()
c = MyCtrl(m,v)
gtk.main()



