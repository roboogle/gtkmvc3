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



# ----------------------------------------------------------------------
# In this example the use of observable properties is shown.
# The example does not need a view and a controller, as only
# the model side (and an observer) is used. 
# ----------------------------------------------------------------------
"""
Test should print:
int changed!
a_list before change! [] append (10,) {}
a_list after change! [10] append None (10,) {}
a_list before change! [10] __setitem__ (0, 11) {}
a_list after change! [11] __setitem__ None (0, 11) {}
a_map before change! {} __setitem__ ('hello', 30) {}
a_map after change! {'hello': 30} __setitem__ None ('hello', 30) {}
a_map before change! {'hello': 30} update ({'bye': 50},) {}
a_map after change! {'bye': 50, 'hello': 30} update None ({'bye': 50},) {}
a_map before change! {'bye': 50, 'hello': 30} __delitem__ ('hello',) {}
a_map after change! {'bye': 50} __delitem__ None ('hello',) {}
"""

import _importer
from gtkmvc import ModelMT
from gtkmvc import Observer


# ----------------------------------------------------------------------
class MyModel (ModelMT):
    """Since version 1.0.0, both maps and lists are allowed as
    observable properties. When changed, observers' methods
    property_<name>_{before,after}_change will be called if found."""
    
    int = 0
    a_list = []
    a_map = {}
    __observables__ = ("a_*", "int")

    def __init__(self):
        ModelMT.__init__(self)
        return    

    pass


# ----------------------------------------------------------------------
class MyObserver (Observer):
    """Since version 1.0.0, base class 'Observer' is provided to
    create observers that are not necessarily derived from Controller"""

    def __init__(self, model):
        Observer.__init__(self, model)
        return

    # notifications

    def property_int_value_change(self, model, old, new):
        print "int changed!"
        return

    def property_a_list_value_change(self, model, old, new):
        print "a_list changed!"
        return

    def property_a_list_before_change(self, model, instance, name,
                                      args, kwargs):
        print "a_list before change!", instance, name, args, kwargs
        return

    def property_a_list_after_change(self, model, instance, name, res,
                                     args, kwargs):
        print "a_list after change!", instance, name, res, args, kwargs
        return

    def property_a_map_before_change(self, model, instance, name,
                                     args, kwargs):
        print "a_map before change!", instance, name, args, kwargs
        return

    def property_a_map_after_change(self, model, instance, name, res,
                                    args, kwargs):
        print "a_map after change!", instance, name, res, args, kwargs
        return

    pass


# Look at what happens to the observer
if __name__ == "__main__":

    m = MyModel()
    c = MyObserver(m)

    # change int:
    m.int = 20

    # change the list:
    m.a_list.append(10)
    m.a_list[0] = m.a_list[0] + 1

    # change the map:
    m.a_map["hello"] = 30
    m.a_map.update({'bye' : 50})
    del m.a_map["hello"]
    pass


