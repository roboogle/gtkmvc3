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
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


import _importer

from gtkmvc3 import View
import gtk

class MyView (View):
    """This handles only the graphical representation of the
    application. The widgets set is built by hand"""

    def __init__(self):
        super(MyView,self).__init__()

        self['window'] = gtk.Window()
        self['window'].set_title("Basic Manual")
        t = gtk.Table(rows=2, columns=2)
        t.set_row_spacings(12)
        t.set_col_spacings(6)

        t.attach(gtk.Label("Counter:"), 0, 1, 0, 1)
        t.attach(gtk.Label("Reset Value:"), 0, 1, 1, 2)
        self['label_val'] = gtk.Label()
        t.attach(self['label_val'], 1, 2, 0, 1)
        self['sb_reset'] = gtk.SpinButton()
        self['sb_reset'].set_numeric(True)
        self['sb_reset'].set_range(0, 100)
        self['sb_reset'].set_increments(1, 10)
        
        
        t.attach(self['sb_reset'], 1, 2, 1, 2)

        b = gtk.HButtonBox()
        b.set_layout(gtk.BUTTONBOX_SPREAD)
        self['button_reset'] = gtk.Button("Reset")
        b.add(self['button_reset'])
        self['button_inc'] = gtk.Button("Increment")
        b.add(self['button_inc'])
        
        h = gtk.VBox(spacing=12)
        h.pack_start(t)
        h.pack_start(gtk.HSeparator(), expand=False)
        h.pack_start(b)
        
        self['window'].add(h)
        self['window'].show_all()
        return

    def set_counter_value(self, val):
        self['label_val'].set_markup("<big><b>%d</b></big>" % val)
        return

    def set_reset_value(self, val):
        self['sb_reset'].set_value(val)
        return

    pass # end of class
