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



# ----------------------------------------------------------------------
# In this example the use of observable properties is shown.
# The example does not need a view and a controller, as only
# the model side (and an observer) is used. 
# ----------------------------------------------------------------------

import _importer
from gtkmvc3 import Model
from gtkmvc3 import Observer


# ----------------------------------------------------------------------
class MyModel (Model):
    """Since version 1.0.0, both maps and lists are allowed as
    observable properties. When changed, observers' notification
    methods will be called."""

    a_int = 0
    a_list = []
    a_map = {}

    __observables__ = ["a_*"]
    pass


# ----------------------------------------------------------------------
class MyObserver (Observer):
    """Since version 1.0.0, base class 'Observer' is provided to
    create observers that are not necessarily derived from Controller"""

    # notifications
    @Observer.observe("a_int", assign=True)
    @Observer.observe("a_list", assign=True)
    def value_change(self, model, prop_name, info):
        print prop_name, "changed!"
        return

    @Observer.observe("a_list", before=True, after=True)
    @Observer.observe("a_map", before=True, after=True)
    def method_call(self, model, prop_name, info):
        if "before" in info: ntype="before"
        else: ntype="after"
        
        print prop_name, ntype, "change!", info.instance, \
              info.method_name, info.args, info.kwargs
        return

    pass


# Look at what happens to the observer
if __name__ == "__main__":

    m = MyModel()
    c = MyObserver(m)

    # change int:
    m.a_int = 20

    # change the list:
    m.a_list.append(10)
    m.a_list[0] = m.a_list[0] + 1

    # change the map:
    m.a_map["hello"] = 30
    m.a_map.update({'bye' : 50})
    del m.a_map["hello"]
    pass


