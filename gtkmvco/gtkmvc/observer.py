#  -------------------------------------------------------------------------
#  Author: Roberto Cavada <cavada@irst.itc.it>
#
#  Copyright (C) 2006 by Roberto Cavada
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
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.
#  -------------------------------------------------------------------------


class Observer (object):
    """Use this class as base class of all observers"""
    
    def __init__(self, model=None):
        self.model = None
        self.register_model(model)
        return

    def register_model(self, model):
        self.unregister_model()
        self.model = model
        if self.model: self.model.register_observer(self)
        return

    def unregister_model(self):
        if self.model:
            self.model.unregister_observer(self)
            self.model = None
            pass
        return

    def __del__(self):
        self.unregister_model()
        return

    def get_model(self): return self.model

    pass # end of class

    
        
