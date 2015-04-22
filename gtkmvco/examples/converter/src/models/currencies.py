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

from currency import CurrencyModel

from gtkmvc3 import ListStoreModel
import os.path
import gobject

import xml.parsers.expat


class CurrenciesModel (ListStoreModel):
    """Model the currencies set. If a model is loaded from file, the
    file is kept aligned if the model is changed later"""

    def __init__(self, filename=None):

        ListStoreModel.__init__(self, gobject.TYPE_PYOBJECT # currency model
                                );
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.__start_element
        self.parser.EndElementHandler = self.__end_element
        self.parser.CharacterDataHandler = self.__char_data

        self.__init_parser()
        
        self.load(filename)        
        return

    def add(self, model):
        """raises an exception if the model cannot be added"""
        def foo(m, p, i):
            if m[i][0].name == model.name:
                raise ValueError("Model already exists")
            return
        # checks if already existing
        self.foreach(foo)
        
        self.append((model,))
        return


    def load(self, filename):
        self.filename = filename
        if filename is None: return

        f = open(self.filename, "r")
        self.parser.ParseFile(f)
        return



    # ----------------------------
    #   Private methods
    # ----------------------------
    def __init_parser(self):
        self.__elem_stack = []
        self.__curr_data = ""
        self.__elems = {
            "name" : None,
            "rate" : None,
            "notes" : None,
            }
            
        return


    def __start_element(self, name, attrs):
        self.__elem_stack.append(name)
        self.__curr_data = ""
        return

    def __end_element(self, name):
        top = self.__elem_stack.pop()
        assert(top == name)

        if name in self.__elems:
            self.__elems[name] = self.__curr_data.strip()
            self.__curr_data = ""
            
        elif name == "currency":
            m = CurrencyModel(self.__elems["name"],
                              float(self.__elems["rate"]),
                              self.__elems["notes"])
            self.add(m)

        else: assert(name == "currencies")
        
        return

    def __char_data(self, data):
        self.__curr_data += data
        return

    pass # end of class
