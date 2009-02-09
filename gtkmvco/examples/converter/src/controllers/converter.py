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
#  or email to the author <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.


import utils._importer
from amount import AmountCtrl

from gtkmvc import Controller

class ConverterCtrl (Controller):
    """Controller of the converter""" 

    def __init__(self, model, view):
        Controller.__init__(self, model, view)

        self.source = AmountCtrl(model.source, view.source)
        self.target = AmountCtrl(model.target, view.target)
        
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""

        # if stand-alone, connects the window delete event to
        # kill the loop
        if self.view.is_stand_alone():
            import gtk
            self.view.get_top_widget().connect('delete-event',
                 lambda w,e: gtk.main_quit())
            pass
        
        return

    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------
    def on_button_convert_clicked(self, btn):
        self.model.convert()
        return

    
    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    def property_can_convert_value_change(self, m, old, new):
        if old != new: self.view['button_convert'].set_sensitive(new)
        return
    
    pass # end of class


