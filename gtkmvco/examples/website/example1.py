#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2006 by Roberto Cavada
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
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.


import _importer, gtkmvc
class MyModel (gtkmvc.Model):
    name = "Roberto"
    age = 0
    __observables__ = ( "name", "age" ) 

    def show(self): print "MyModel: name=", self.name, "age=", self.age
    pass # end of class

import gtk
class MyView (gtkmvc.View): pass # end of class

class MyCtrl (gtkmvc.Controller):    
    def on_button_clicked(self, button):
        self.model.show()
        return

    def on_window_delete_event(self, window, event):
        # quits the application
        gtk.main_quit()
        return True
    pass # end of class

# Application parts construction and launch
m = MyModel()
v = MyView(glade="example1.glade")
c = MyCtrl(m, v, auto_adapt=True)
gtk.main() # run the application

