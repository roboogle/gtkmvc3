#  Author: Roberto Cavada <roboogle@gmail.com>
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
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


import _importer
from gtkmvc import Controller


class MyCtrl (Controller):
    """Handles signal processing, and keeps alignment of model and
    view"""

    def register_view(self, view):
        # sets initial values for the view
        self.view.set_counter_value(self.model.counter)
        self.view.set_reset_value(self.model.reset_value)
        return

    # gtk signals
    def on_window_delete_event(self, window, event):
        import gtk
        gtk.main_quit()
        return True

    def on_button_inc_clicked(self, button):
        self.model.counter += 1
        return

    def on_button_reset_clicked(self, button):
        self.model.reset()
        return

    def on_sb_reset_value_changed(self, sb):
        self.model.reset_value = sb.get_value_as_int()
        return
    
    # observable properties
    @Controller.observe("counter", assign=True)
    def counter_change(self, model, prop_name, info):
        self.view.set_counter_value(info.new)
        return
    
    pass # end of class
