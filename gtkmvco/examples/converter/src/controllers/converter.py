#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006-2015 by Roberto Cavada
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
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


import utils._importer
from amount import AmountCtrl

from gtkmvc3 import Controller

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
    @Controller.observe("can_convert", assign=True)
    def can_convert_change(self, m, pname, info):
        if info.old != info.new:
            self.view['button_convert'].set_sensitive(info.new)
            pass
        return
    
    pass # end of class


