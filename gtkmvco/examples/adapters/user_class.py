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
from gtkmvc3 import Model, Controller, View, Observable
from gtkmvc3.adapters import UserClassAdapter

import gtk


# This example makes use of a user-defined class that contains a
# setter and a getter for an internal variable. When the class is
# instantiated, a maximum value is specified. That limit represents
# the maximum value that the internal variable can be set at.
#
# The controller declares an adapter that adapts a text entry and
# the user-class instance. As the user class raises a ValueError
# exception when trying setting a bad value, the adapter is
# requested to handle error conditions through value_error
# parameter. Try to set a value greater than 10 by editing the text
# entry.

class UserClass (Observable):
    def __init__(self, max_val):
        Observable.__init__(self)
        self.__x = 0
        self.max_val = max_val
        return

    @Observable.observed
    def set_x(self, v):
        if v > self.max_val:
            raise ValueError("x cannot be greater than %d" % self.max_val)
        self.__x=v
        return
        
    def get_x(self): return self.__x
    pass


class MyView (View):
    glade = "adapters.glade"
    top = "window2"
    pass


class MyModel (Model):
    xx = UserClass(10)
    __observables__ = ("xx",)
    pass


class MyCtrl (Controller):
    def register_adapters(self):
        a = UserClassAdapter(self.model, "xx", "get_x", "set_x",
                             value_error=myerr)
        a.connect_widget(self.view["en2"])
        self.adapt(a)
        return

    def on_button2_clicked(self, button):
        self.model.xx.set_x(self.model.xx.get_x() + 1)
        return 

    def on_window2_delete_event(self, w, e):
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
c = MyCtrl(m, v)

m.xx.set_x(5)

gtk.main()



