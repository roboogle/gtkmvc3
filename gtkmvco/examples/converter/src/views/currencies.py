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
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import utils._importer
from gtkmvc import View

from currency import CurrencyView

import utils.globals
import os.path
import gtk

# ----------------------------------------------------------------------
class CurrenciesView (View):
    """This is the view for the 'Currencies' dialog"""
    
    GLADE_FILE = os.path.join(utils.globals.GLADE_DIR, "converter.glade") 

    def __init__(self, ctrl):
        View.__init__(self, ctrl, self.GLADE_FILE, "dialog_currencies")
        return

    def add_currency_view(self, curr_ctrl, select=False):
        v = CurrencyView(curr_ctrl)
        self.remove_currency_view()
        self['hbox_top'].pack_end(v.get_top_widget())
        v.light_name(select)
        return

    def remove_currency_view(self):
        hbox = self['hbox_top']
        ch = hbox.get_children()
        if len(ch) > 1: hbox.remove(ch[-1])
        return

    def destroy(self):
        self['dialog_currencies'].destroy()
        return
    
    pass # end of class
# ----------------------------------------------------------------------
