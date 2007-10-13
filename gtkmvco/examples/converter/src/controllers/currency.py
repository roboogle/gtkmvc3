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
#  or email to the author <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import utils._importer
from gtkmvc import Controller
import gtk

class CurrencyCtrl (Controller):
    """Controller of a Currency. gtk signals and observer align the
    model content and the view content.""" 

    def __init__(self, model):
        Controller.__init__(self, model)
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
    def property_name_value_change(self, m, old, new):
        if old != new and not self.__changing: self.view.set_name(new)
        return

    def property_rate_value_change(self, m, old, new):
        if old != new and not self.__changing: self.view.set_rate(new)
        return

    def property_notes_value_change(self, m, old, new):
        if old != new and not self.__changing: self.view.set_notes(new)
        return
    
    pass # end of class


