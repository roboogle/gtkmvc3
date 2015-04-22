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

from amount import AmountModel
from gtkmvc3 import Model

class ConverterModel (Model):
    can_convert = False
    __observables__ = ("can_convert",)

    def __init__(self, currencies_model):
        Model.__init__(self)

        self.source = AmountModel(currencies_model)
        self.target = AmountModel(currencies_model)

        self.observe_model(self.source)
        self.observe_model(self.target)
        return

    def convert(self):
        if not self.can_convert: return
        srate = self.source.get_currency().rate        
        crate = self.target.get_currency().rate
        self.target.amount = self.source.amount * (crate / srate)
        return
        
    
    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    @Model.observe("iter", assign=True)
    def iter_value_change(self, model, _, info):
        assert model in (self.source, self.target)
        self.can_convert = (self.source.iter is not None and
                            self.target.iter is not None)
        return
        
    pass # end of class
