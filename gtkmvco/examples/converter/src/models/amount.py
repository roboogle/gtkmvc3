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

from gtkmvc3 import Model


class AmountModel (Model):
    """This model represents a single pair of amount/currency. The
    model contains: the model of the available currencies, the amount,
    and an iterator within the currencies model pointing to the
    currently selected currency which the amount refer to."""

    amount = 0.0
    iter = None
    __observables__ = ("amount", "iter")
    
    def __init__(self, currencies_model):
        Model.__init__(self)
        
        self.currencies = currencies_model
        return

    def get_currency(self):
        if self.iter is None: return None
        return self.currencies[self.iter][0]
    
    pass # end of class
