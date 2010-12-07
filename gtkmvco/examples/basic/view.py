#  Author: Roberto Cavada <roboogle@gmail.com>
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
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


import _importer

from gtkmvc import View

class MyView (View):
    """This handles only the graphical representation of the
    application. The widgets set is loaded from glade file"""
    
    glade = "basic.glade"

    def set_counter_value(self, val):
        self['label_val'].set_markup("<big><b>%d</b></big>" % val)
        return

    def set_reset_value(self, val):
        self['sb_reset'].set_value(val)
        return

    pass # end of class
