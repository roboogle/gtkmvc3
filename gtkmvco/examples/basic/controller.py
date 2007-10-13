#  Author: Roberto Cavada <cavada@irst.itc.it>
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
#  or email to the author Roberto Cavada <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import _importer
from gtkmvc import Controller


class MyCtrl (Controller):
    """Handles signal processing, and keeps alignment of model and
    view"""
    def __init__(self, model):
        Controller.__init__(self, model)
        return

    def register_view(self, view):
        Controller.register_view(self, view)

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
    
    def property_counter_value_change(self, model, old, new):
        self.view.set_counter_value(new)
        return
    
    pass # end of class
