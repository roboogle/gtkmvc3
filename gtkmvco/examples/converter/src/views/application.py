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
import utils.globals
from converter import ConverterView

from gtkmvc import View

import os.path


# ----------------------------------------------------------------------
class ApplicationView (View):
    """A view for the top level window (application)"""
    
    GLADE_FILE = os.path.join(utils.globals.GLADE_DIR, "converter.glade")

    def __init__(self, ctrl):
        View.__init__(self, ctrl, self.GLADE_FILE, 'window_app')

        self.converter = None        
        return

    def create_sub_views(self, conv_ctrl):
        # creates and connects sub views
        self.converter = ConverterView(conv_ctrl, False) # not a top level
        vbox = self['vbox_top']
        vbox.pack_start(self.converter.get_top_widget())
        return

    pass # end of class
# ----------------------------------------------------------------------
