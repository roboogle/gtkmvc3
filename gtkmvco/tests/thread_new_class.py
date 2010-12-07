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
# In this example the use of observable properties is shown.  In the
# other example 'existing_object' an already defined (and
# instantiated) object was observed. Instead, in this example we want
# to develop a class that represents an observable object by
# construction, i.e. designed to be integrated in the observable
# pattern of gtkmvc. This can be easily achieved by deriving our class
# from the Observable base class, and by declaring the methods that we
# want to monitor (for example, those that change the class instance)
# by using a decorator.
# ----------------------------------------------------------------------
"""
Test should print:
obj after change! <id 1> change None (<id 1>,) {}
"""


import _importer

from gtkmvc import ModelMT as Model
from gtkmvc import Observer, Observable
from gtkmvc import observable 

# ----------------------------------------------------------------------
class AdHocClass (Observable):

    """This is a class that is thought to be integrated into the
    observer pattern. It is declared to be 'observable' and the
    methods which we are interested in monitoring are decorated
    accordingly"""

    def __init__(self):
        Observable.__init__(self)
        self.val = 0
        pass
    
    @Observable.observed # this way the method is declared as 'observed'
    def change(self): self.val += 1

    pass #end of class


# ----------------------------------------------------------------------
class MyModel (Model):

    obj = AdHocClass()
    __observables__ = ("obj",)

    def __init__(self):
        Model.__init__(self)
        return    

    pass # end of class


# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model):
        Observer.__init__(self, model)
        return

    # notification
    def property_obj_value_change(self, model, old, new):
        print "obj changed!"
        return

    # we are interested in knowing the object changed only after it
    # had changed, so property_obj_before_change is not defined, and
    # will not be called.
    def property_obj_after_change(self, model, instance, name, res,
                                  args, kwargs):
        print "obj after change!", instance, name, res, args, kwargs
        return

    pass

# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.obj.change()
    pass
# ----------------------------------------------------------------------

