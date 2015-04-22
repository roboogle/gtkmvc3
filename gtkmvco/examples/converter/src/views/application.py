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
import utils.globals
from converter import ConverterView

from gtkmvc3 import View

import os.path


# ----------------------------------------------------------------------
class ApplicationView (View):
    """A view for the top level window (application)"""
    
    glade = os.path.join(utils.globals.GLADE_DIR, "app.glade")
    top = 'window_app'
    def __init__(self):
        View.__init__(self)

        self.converter = ConverterView(False) # not a top level

        vbox = self['vbox_top']
        vbox.pack_start(self.converter.get_top_widget())
        return

    pass # end of class
# ----------------------------------------------------------------------
