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
# In this example the use of observable properties is shown.  In the
# other example 'existing_object' an already defined (and
# instantiated) object was observed. Instead, in this example we want
# to develop a class that represents an observable object by
# construction, i.e. designed to be integrated in the observable
# pattern of gtkmvc3. This can be easily achieved by deriving our class
# from the Observable base class, and by declaring the methods that we
# want to monitor (for example, those that change the class instance)
# by using a decorator.
# ----------------------------------------------------------------------


import _importer

import _importer
from gtkmvc3 import Model, Observer, Observable

# ----------------------------------------------------------------------
class AdHocClass (Observable):

    """This is a class that is thought to be integrated into the
    observer pattern. It is declared to be 'observable' and the
    methods which we are interested in monitoring are decorated
    accordingly"""

    def __init__(self): 
        Observable.__init__(self)
        self.val = 0
        return

    @Observable.observed # this way the method is declared as 'observed'
    def change(self): self.val += 1

    pass #end of class


# ----------------------------------------------------------------------
class MyModel (Model):

    obj = AdHocClass()
    __observables__ = ("obj",)

    pass # end of class


# ----------------------------------------------------------------------
class MyObserver (Observer):

    # notification
    # we are interested in knowing the object changed only after it
    # had changed, so 'before' is not set
    @Observer.observe("obj", assign=True, after=True)
    def property_obj_value_change(self, model, prop_name, info):
        if "assign" in info:
            print prop_name, "changed!"
        else:
            assert "after" in info
            print prop_name, "after change!", info.instance, \
                  info.method_name, info.res, info.args, info.kwargs
            pass
        return

    pass

# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.obj.change()
    pass
# ----------------------------------------------------------------------

