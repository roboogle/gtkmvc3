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
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import utils._importer
from gtkmvc import Controller
import gtk

class AmountCtrl (Controller):
    """Controller of a single 'amount' (see AmountModel)""" 

    def __init__(self, model):
        Controller.__init__(self, model)

        self.__changing_amount = False
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""
        Controller.register_view(self, view)

        self.setup_combobox()
        return

    def setup_combobox(self):
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
    def property_amount_value_change(self, m, old, new):
        if self.__changing_amount: return
        self.view['sb_amount'].set_value(new)
        return
    pass # end of class


