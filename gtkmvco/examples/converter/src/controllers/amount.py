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

class AmountCtrl (Controller):
    """Controller of a single 'amount' (see AmountModel)""" 

    def __init__(self, model, view):
        Controller.__init__(self, model, view)

        self.__changing_amount = False
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""
        cb = self.view['cb_currency']
        cb.set_model(self.model.currencies)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        
        def on_cell_data(cb, cell, mod, it):
            if mod[it][0]: cell.set_property('text', mod[it][0].name)
            return

        cb.set_cell_data_func(cell, on_cell_data)
        return

    # ----------------------------------------
    #               callbacks
    # ----------------------------------------

    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------
    def on_sb_amount_value_changed(self, sb):
        self.__changing_amount = True
        self.model.amount = sb.get_value()
        self.__changing_amount = False
        return

    def on_cb_currency_changed(self, cb):
        self.model.iter = cb.get_active_iter()        
        return
    
    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    @Controller.observe("amount", assign=True)
    def amount_change(self, m, n, info):
        if self.__changing_amount: return
        self.view['sb_amount'].set_value(info.new)
        return
    pass # end of class


