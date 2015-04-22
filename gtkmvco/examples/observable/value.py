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

    internal = 0

    # external_spec here is a property that is not stored internally, but
    # handled by a pair of methods (a getter and a setter)
    # external_gen instead does not have a specific pair of getter/setter, but
    # its values are got and set by a general methods pair.
    __observables__ = ["internal", "external_spec", "external_gen"]

    @Model.getter
    def get_external_spec(self): return "some value for external_spec"

    @Model.setter
    def set_external_spec(self, val):
        print "specific setter has been called"
        return

    @Model.getter("external_gen")
    def get__value(self, name): return "some value for generic " + name

    @Model.setter("external_gen")
    def set__value(self, name, value):
        print "generic setter for %s has been called" % name
        return
    
    pass


# ----------------------------------------------------------------------
class MyObserver (Observer):
    """Since version 1.0.0, base class 'Observer' is provided to
    create observers that are not necessarily derived from Controller"""

    # notifications
    @Observer.observe("internal", assign=True)
    @Observer.observe("external_spec", assign=True)
    @Observer.observe("external_gen", assign=True)
    def value_change(self, model, prop_name, info):
        print prop_name, "changed!"
        return
    
    pass


# Look at what happens to the observer
if __name__ == "__main__":

    m = MyModel()
    c = MyObserver(m)

    m.internal = 20
    m.external_spec = "a new value"
    m.external_gen = "a new value"

    a = m.external_gen
    print a
    pass


