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
from converter import ConverterCtrl

from currencies import CurrenciesCtrl
from views.currencies import CurrenciesView

from about import AboutCtrl
from views.about import AboutView

from gtkmvc3 import Controller

import gtk

class ApplicationCtrl (Controller):
    """Controller of the top-level window (application)""" 

    def __init__(self, model, view):
        Controller.__init__(self, model, view)
        self.converter = ConverterCtrl(model.converter, view.converter)
        self.currencies = None
        return

    def quit(self):
        gtk.main_quit()
        return
    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------
    def on_tb_editor_clicked(self, tb):
        v = CurrenciesView()
        self.currencies = CurrenciesCtrl(self.model.currencies, v)
        return
        
    def on_tb_about_clicked(self, tb):        
        v = AboutView()
        c = AboutCtrl(self.model.about, v)
        v.run() # this runs in modal mode
        return

    def on_window_app_delete_event(self, w, e):
        self.quit()
        return True

    def on_tb_quit_clicked(self, bt): self.quit()
        
    
    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    
    pass # end of class


