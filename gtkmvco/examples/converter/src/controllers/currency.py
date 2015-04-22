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
from gtkmvc3 import Controller
import gtk

class CurrencyCtrl (Controller):
    """Controller of a Currency. gtk signals and observer align the
    model content and the view content.""" 

    def __init__(self, model, view):
        Controller.__init__(self, model, view)
        self.__changing = False
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""
        Controller.register_view(self, view)

        # connects additional signals
        self.view['tv_notes'].get_buffer().connect("changed",
                                          self.on_notes_changed)

        # Sets initial values for the view.
        # Later observer will keep the view always aligned
        self.view.set_name(self.model.name)
        self.view.set_rate(self.model.rate)
        self.view.set_notes(self.model.notes)
        return

    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------

    def on_entry_name_changed(self, entry):
        self.__changing = True
        self.model.name = self.view.get_name()
        self.__changing = False
        return

    def on_sb_rate_value_changed(self, entry):
        self.__changing = True
        self.model.rate = self.view.get_rate()
        self.__changing = False
        return

    def on_notes_changed(self, textbuf):
        self.__changing = True
        self.model.notes = self.view.get_notes()
        self.__changing = False
        return


    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    @Controller.observe("name", assign=True)
    @Controller.observe("rate", assign=True)
    @Controller.observe("notes", assign=True)
    def value_change(self, m, prop_name, info):
        if info.old != info.new and not self.__changing:
            meth = { "name" : self.view.set_name,
                     "rate" : self.view.set_rate,
                     "notes" : self.view.set_notes,
                     }[prop_name]
            meth(info.new)
            pass
        return
    
    pass # end of class


